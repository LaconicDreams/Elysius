"""Balance auditor: reads every shop price and quest reward and flags the outliers.

Everything is converted to one currency, "iron" (1 = one iron ingot), using the VALUES table below.
Items without a base value get one from the cheapest shop that sells them (ammo, guns, attachments,
rockets), so a reward of "gun:ak47, 120 ammo:762x39" is worth what those would cost in the shops.

Checks:
  * bulk trades that are worse per unit than the single trade
  * shop text that disagrees with what the quest really asks or gives
  * guns that cost less than a few magazines of their own ammo, or whose ammo is sold nowhere
  * guns priced far from other guns of the same type (per point of damage per second)
  * ammo and attachment prices far from the rest of their chapter
  * one-off quests that pay out more than the items they take
  * kill bounties paying far more or less per unit of effort than the others
  * later quests in a chain paying less than the one before, dimension bounties that don't scale up
  * trade loops that create items from nothing, and creative-only items given as rewards

Usage: py balance.py            (report is also saved to balance_report.txt)
Tune VALUES, MOB_EFFORT and the thresholds below to taste.
"""

import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
import snbt  # noqa: E402

REPORT = os.path.join(HERE, "balance_report.txt")

# ---------------------------------------------------------------- tuning
# Base worth of raw materials, in iron ingots.
VALUES = {
    "minecraft:iron_ingot": 1, "minecraft:copper_ingot": 0.3, "minecraft:gold_ingot": 2,
    "minecraft:diamond": 8, "minecraft:emerald": 6, "minecraft:netherite_ingot": 80,
    "minecraft:netherite_scrap": 18, "minecraft:redstone": 0.2, "minecraft:lapis_lazuli": 0.3,
    "minecraft:glass": 0.15, "minecraft:leather": 0.5, "minecraft:gunpowder": 0.5, "minecraft:bone": 0.2,
    "minecraft:rotten_flesh": 0.05, "minecraft:quartz": 0.3, "minecraft:glowstone_dust": 0.3,
    "minecraft:amethyst_shard": 0.5, "minecraft:crying_obsidian": 3, "minecraft:end_crystal": 20,
    "minecraft:blaze_rod": 2, "minecraft:fire_charge": 1, "minecraft:stick": 0.02,
    "minecraft:white_wool": 0.2, "minecraft:cooked_beef": 0.3, "minecraft:cooked_porkchop": 0.3,
    "minecraft:golden_apple": 18, "minecraft:enchanted_golden_apple": 150, "minecraft:totem_of_undying": 40,
    "minecraft:shulker_shell": 10, "minecraft:shulker_box": 22, "minecraft:nether_star": 150,
    "minecraft:written_book": 0, "minecraft:elytra": 100, "minecraft:netherite_chestplate": 150,
    "travelersbackpack:standard": 12,
}
# any item whose id matches one of these patterns
VALUE_PATTERNS = [
    (r"^minecraft:\w+_shulker_box$", 22),
    (r"^travelersbackpack:\w+_upgrade$", 16),
]
# Rough effort per kill (1 = a zombie).
MOB_EFFORT = {
    "minecraft:zombie": 1, "minecraft:skeleton": 1, "minecraft:spider": 1, "minecraft:creeper": 1.5,
    "minecraft:enderman": 2, "minecraft:blaze": 2.5, "minecraft:wither_skeleton": 3, "minecraft:pillager": 1.5,
    "minecraft:ravager": 12, "minecraft:hoglin": 3, "minecraft:piglin_brute": 6, "minecraft:phantom": 2,
    "minecraft:ghast": 5, "minecraft:elder_guardian": 40, "minecraft:wither": 150, "minecraft:ender_dragon": 200,
    "minecraft:warden": 120, "minecraft:shulker": 3,
    "aether:zephyr": 2, "aether:cockatrice": 3, "aether:sentry": 2, "aether:slider": 50,
    "aether:sun_spirit": 120, "aether:valkyrie_queen": 80,
}
GUN_MAGS_OF_AMMO = 3     # a gun should cost at least this many magazines of its ammo
OUTLIER = 2.5            # flag prices more than this many times above (or below 1/OUTLIER) the median
KILL_OUTLIER = 3.0       # same, for kill bounties' reward per unit of effort
ONE_OFF_MARGIN = 1.5     # a one-off item trade may pay out up to this much more than it takes


# ---------------------------------------------------------------- item helpers

def key_of(item):
    """A stable key for valuing an item: 'gun:tacz:ak47', 'ammo:tacz:9mm', 'att:...', or the item id."""
    if isinstance(item, str):
        return item
    iid, tag = item.get("id"), item.get("tag") or {}
    if iid == "tacz:modern_kinetic_gun" and "GunId" in tag:
        return "gun:" + tag["GunId"]
    if iid == "tacz:ammo" and "AmmoId" in tag:
        return "ammo:" + tag["AmmoId"]
    if iid == "tacz:attachment" and "AttachmentId" in tag:
        return "att:" + tag["AttachmentId"]
    return iid


def creative_flag(item):
    if isinstance(item, dict):
        tag = item.get("tag") or {}
        return any("creative" in k.lower() for k in tag)
    return False


class Shop:
    def __init__(self, chapter, quest):
        self.chapter, self.quest = chapter, quest
        self.title = quest.get("title", "?").replace("\\&", "&")
        self.inputs = [(key_of(t["item"]), int(t.get("count", 1))) for t in quest["tasks"]]
        out = {}
        for r in quest["rewards"]:
            k = key_of(r["item"])
            out[k] = out.get(k, 0) + int(r.get("count", 1))
        self.outputs = out

    def label(self):
        return f"{self.chapter}: {self.title}"


def is_shop(q):
    tasks, rewards = q.get("tasks", []), q.get("rewards", [])
    return (q.get("can_repeat") and tasks and rewards
            and all(t.get("type") == "item" and t.get("consume_items") for t in tasks)
            and all(r.get("type") == "item" for r in rewards))


class Valuer:
    def __init__(self, shops):
        self.base = dict(VALUES)
        self.derived = {}   # key -> (unit value, shop)
        self.unknown = set()
        for _ in range(6):  # repeat so items bought with shop-made items get a value too
            changed = False
            for s in shops:
                cost = self.total(s.inputs, record=False)
                if cost is None or len(s.outputs) != 1:
                    continue
                (k, n), = s.outputs.items()
                unit = cost / n
                if k in self.base:
                    continue
                if k not in self.derived or unit < self.derived[k][0] - 1e-9:
                    self.derived[k] = (unit, s)
                    changed = True
            if not changed:
                break

    def unit(self, key, record=True):
        if key in self.base:
            return self.base[key]
        if key in self.derived:
            return self.derived[key][0]
        for pat, v in VALUE_PATTERNS:
            if re.match(pat, key):
                return v
        if record:
            self.unknown.add(key)
        return None

    def total(self, pairs, record=True):
        tot = 0.0
        for k, n in pairs:
            u = self.unit(k, record)
            if u is None:
                return None
            tot += u * n
        return tot

    def rewards(self, quest):
        pairs, missing = [], []
        for r in quest.get("rewards", []):
            if r.get("type") != "item":
                continue
            k, n = key_of(r["item"]), int(r.get("count", 1))
            if self.unit(k) is None:
                missing.append(k)
            else:
                pairs.append((k, n))
        return self.total(pairs) or 0.0, missing


def fmt(v):
    if v is None:
        return "?"
    if v >= 100:
        return f"{v:,.0f}"
    if v >= 10:
        return f"{v:.1f}"
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- audit

def audit():
    gd = gamedata.load()
    chapters_dir = os.path.join(gamedata.QUESTS_DIR, "chapters")
    groups = {g["id"]: g["title"] for g in
              snbt.load(os.path.join(gamedata.QUESTS_DIR, "chapter_groups.snbt"))["chapter_groups"]}
    chapters = []
    for f in sorted(os.listdir(chapters_dir)):
        if f.endswith(".snbt"):
            chapters.append(snbt.load(os.path.join(chapters_dir, f)))

    shops, one_offs = [], []
    for c in chapters:
        for q in c["quests"]:
            (shops if is_shop(q) else one_offs).append((c, q))
    shop_objs = [Shop(c["filename"], q) for c, q in shops]
    val = Valuer(shop_objs)
    findings = []

    def flag(level, area, where, msg):
        findings.append((level, area, where, msg))

    def name(key):
        kind, _, rid = key.partition(":")
        if kind in ("gun", "ammo", "att"):
            return gd.tacz_name({"att": "attachment"}.get(kind, kind), rid) or rid
        return gd.item_name(key)

    # 1. bulk vs single
    by_out = {}
    for s in shop_objs:
        if len(s.outputs) == 1:
            (k, n), = s.outputs.items()
            cost = val.total(s.inputs, record=False)
            if cost is not None:
                # only compare trades that pay with the same items (single vs bulk of one trade)
                currency = tuple(sorted(i for i, _ in s.inputs))
                by_out.setdefault((k, currency), []).append((n, cost / n, s))
    for (k, _), offers in by_out.items():
        offers.sort(key=lambda o: o[0])
        for small, big in zip(offers, offers[1:]):
            if big[0] > small[0] and big[1] > small[1] * 1.001:
                flag("WARN", "Shop", big[2].label(),
                     f"bulk trade costs {fmt(big[1])} per {name(k)}, the single trade only {fmt(small[1])}. "
                     f"Bulk should never be worse")

    # 2. text vs actual numbers
    for s in shop_objs:
        desc = [d.replace("\\&", "&") for d in s.quest.get("description", [])]
        if not desc:
            continue
        first = desc[0]
        if "=" in first:
            left, right = first.split("=", 1)
            said_in = [int(x) for x in re.findall(r"\d+(?=x?\s+[A-Za-z])", left)]
            said_out = [int(x) for x in re.findall(r"(\d+)\s+(?:rounds?|rockets?)", right)]
            real_in = [n for _, n in s.inputs]
            real_out = sum(s.outputs.values())
            if said_in and sorted(said_in) != sorted(real_in):
                flag("WARN", "Text", s.label(), f"text says it costs {said_in}, the quest actually takes {real_in}")
            if said_out and said_out[0] != real_out:
                flag("WARN", "Text", s.label(), f"text says it gives {said_out[0]}, the quest actually gives {real_out}")
        elif first.startswith("Price:"):
            said = sorted(int(x) for x in re.findall(r"(\d+)x?\s+[A-Za-z]", first))
            real = sorted(n for _, n in s.inputs)
            if said != real:
                flag("WARN", "Text", s.label(), f"text says the price is {said}, the quest actually takes {real}")
    for c, q in one_offs:
        for d in q.get("description", []):
            m = re.match(r"Reward: .* with (\d+) rounds", d)
            if m:
                real = sum(int(r.get("count", 1)) for r in q.get("rewards", [])
                           if key_of(r.get("item", "")).startswith("ammo:"))
                if int(m.group(1)) != real:
                    flag("WARN", "Text", f"{c['filename']}: {q.get('title')}",
                         f"text promises {m.group(1)} rounds, the rewards give {real}")

    # 3 + 4. guns
    gun_rows = []
    for k, (unit, s) in val.derived.items():
        if not k.startswith("gun:"):
            continue
        gid = k[4:]
        ammo_id = gd.gun_ammo(gid)
        mag = gd.gun_mag(gid) or 0
        ammo_unit = val.unit("ammo:" + ammo_id, record=False) if ammo_id else None
        if ammo_id and ammo_unit is None:
            flag("WARN", "Guns", s.label(), f"its ammo ({name('ammo:' + ammo_id)}) is not sold in any shop")
        elif ammo_unit and mag:
            supply = GUN_MAGS_OF_AMMO * mag * ammo_unit
            if unit < supply:
                flag("WARN", "Guns", s.label(),
                     f"the gun costs {fmt(unit)} iron but {GUN_MAGS_OF_AMMO} magazines ({GUN_MAGS_OF_AMMO * mag} rounds) "
                     f"of its ammo cost {fmt(supply)}. Ammo, not the gun, is the real price")
        dps = gd.gun_dps(gid)
        gun_rows.append((gd.gun_type(gid) or "other", gid, unit, dps, s))
    sold = {r[1] for r in gun_rows}
    for gid in sorted(gd.guns):
        if gid not in sold:
            flag("INFO", "Guns", "gun_shop", f"{name('gun:' + gid)} ({gid}) is not sold anywhere")
    by_type = {}
    for row in gun_rows:
        by_type.setdefault(row[0], []).append(row)
    for typ, rows in by_type.items():
        per = [(r[2] / r[3], r) for r in rows if r[3]]
        if len(per) < 3:
            continue
        med = statistics.median(p for p, _ in per)
        for p, r in per:
            if p > med * OUTLIER or p < med / OUTLIER:
                word = "expensive" if p > med else "cheap"
                flag("INFO", "Guns", r[4].label(),
                     f"{word} for a {typ}: {fmt(r[2])} iron for {fmt(r[3])} damage/sec "
                     f"({fmt(p)} per dps; other {typ}s median {fmt(med)})")

    for k, (unit, s) in val.derived.items():
        if k.startswith("ammo:") and not gd.guns_using(k[5:]):
            flag("WARN", "Ammo", s.label(), f"no installed gun fires {name(k)}; players can buy ammo they can never use")

    # 5. ammo and attachment outliers within their chapter
    for prefix, area in (("ammo:", "Ammo"), ("att:", "Attachments")):
        per_chapter = {}
        for k, (unit, s) in val.derived.items():
            if k.startswith(prefix):
                per_chapter.setdefault(s.chapter, []).append((unit, k, s))
        for ch, rows in per_chapter.items():
            if len(rows) < 4:
                continue
            med = statistics.median(u for u, _, _ in rows)
            for u, k, s in rows:
                if u > med * OUTLIER or u < med / OUTLIER:
                    word = "pricier" if u > med else "cheaper"
                    flag("INFO", area, s.label(), f"{fmt(u)} iron each, {u / med:.1f}x the chapter median "
                                                  f"({fmt(med)}). {word.capitalize()} than its neighbours")

    # 6. one-off quests: payout vs what they take; kill bounties: payout per effort
    kill_rows = []
    rewards_by_id = {}
    for c, q in one_offs:
        where = f"{c['filename']}: {q.get('title')}"
        reward, missing = val.rewards(q)
        rewards_by_id[q["id"]] = (reward, c, q)
        for r in q.get("rewards", []):
            if r.get("type") == "item" and creative_flag(r["item"]):
                flag("WARN", "Rewards", where, f"gives a creative-only item ({key_of(r['item'])}, "
                                               f"{', '.join(k for k in r['item'].get('tag', {}))}). "
                                               f"Unlimited ammo makes the ammo shops pointless")
        keys = [key_of(r["item"]) for r in q.get("rewards", []) if r.get("type") == "item"]
        guns = [k[4:] for k in keys if k.startswith("gun:")]
        ammo_given = {k[5:] for k in keys if k.startswith("ammo:")}
        if guns and ammo_given:
            usable = {gd.gun_ammo(g) for g in guns}
            for a in ammo_given - usable:
                flag("WARN", "Rewards", where, f"gives {name('ammo:' + a)}, but none of the guns in the reward "
                                               f"({', '.join(name('gun:' + g) for g in guns)}) can fire it")
        asks = [(key_of(t["item"]), int(t.get("count", 1))) for t in q.get("tasks", [])
                if t.get("type") == "item" and t.get("consume_items")]
        if asks:
            ask = val.total(asks)
            if ask is not None and reward > ask * ONE_OFF_MARGIN and reward - ask > 4:
                flag("WARN", "Rewards", where, f"pays {fmt(reward)} iron for items worth {fmt(ask)}")
        kills = [t for t in q.get("tasks", []) if t.get("type") == "kill"]
        if kills and len(kills) == len(q.get("tasks", [])) and reward:
            effort = sum(MOB_EFFORT.get(t["entity"], 1) * int(t.get("value", 1)) for t in kills)
            kill_rows.append((reward / effort, reward, effort, where, kills))
    if len(kill_rows) >= 4:
        med = statistics.median(r[0] for r in kill_rows)
        for ratio, reward, effort, where, kills in kill_rows:
            if ratio > med * KILL_OUTLIER or ratio < med / KILL_OUTLIER:
                what = ", ".join(f"{int(t.get('value', 1))} {t['entity'].split(':')[1]}" for t in kills)
                word = "generous" if ratio > med else "stingy"
                flag("WARN", "Bounties", where,
                     f"{word}: {fmt(reward)} iron for {what} ({fmt(ratio)} per effort point; "
                     f"median bounty {fmt(med)}). Adjust MOB_EFFORT if the mob is harder than it looks")

    # 7. chains: a follow-up quest with the same kind of task should not pay less
    for qid, (reward, c, q) in rewards_by_id.items():
        for dep in q.get("dependencies", []):
            if dep not in rewards_by_id:
                continue
            prev, _, pq = rewards_by_id[dep]
            same = ({(t.get("type"), t.get("stat")) for t in q.get("tasks", [])} ==
                    {(t.get("type"), t.get("stat")) for t in pq.get("tasks", [])})
            if same and q.get("tasks", [{}])[0].get("type") == "stat" and reward < prev * 0.95:
                flag("WARN", "Chains", f"{c['filename']}: {q.get('title')}",
                     f"pays {fmt(reward)} iron, less than the step before it ('{pq.get('title')}', {fmt(prev)})")

    # dimension bounties should scale up chapter by chapter
    dims = [c for c in chapters if groups.get(c.get("group")) == "Dimensions"]
    dims.sort(key=lambda c: c.get("order_index", 0))
    avgs = []
    for c in dims:
        vals = [rewards_by_id[q["id"]][0] for q in c["quests"] if q["id"] in rewards_by_id]
        if vals:
            avgs.append((c, statistics.mean(vals)))
    for (a, va), (b, vb) in zip(avgs, avgs[1:]):
        if vb < va:
            flag("WARN", "Chains", b["filename"],
                 f"average bounty {fmt(vb)} iron, less than the previous dimension "
                 f"({a['filename']}, {fmt(va)}). Later dimensions should pay more")

    # 8. loops: buy X with Y, then buy back more Y with X
    for s in shop_objs:
        if len(s.inputs) != 1 or len(s.outputs) != 1:
            continue
        (ik, inn), (ok, on) = s.inputs[0], next(iter(s.outputs.items()))
        for t in shop_objs:
            if t is s or len(t.inputs) != 1 or len(t.outputs) != 1:
                continue
            (ik2, in2), (ok2, on2) = t.inputs[0], next(iter(t.outputs.items()))
            if ik2 == ok and ok2 == ik:
                gain = (on / inn) * (on2 / in2)
                if gain > 1.0001:
                    flag("ERROR", "Loops", s.label(), f"trading through '{t.title}' turns 1 {name(ik)} into "
                                                      f"{gain:.2f}: infinite items")

    if val.unknown:
        flag("INFO", "Values", "balance.py", "no value for: " + ", ".join(sorted(val.unknown)) +
             ". Add them to VALUES so the rewards that use them are counted")

    summary = {
        "shops": len(shop_objs), "one_offs": len(one_offs),
        "prices": {k: v[0] for k, v in val.derived.items()},
        "gun_rows": gun_rows,
    }
    return findings, summary, name


def main(argv=None):
    findings, summary, name = audit()
    out = [f"Balance audit: {summary['shops']} shop trades, {summary['one_offs']} other quests. "
           f"Values in iron ingots (diamond = {VALUES['minecraft:diamond']}, emerald = {VALUES['minecraft:emerald']}, "
           f"gold = {VALUES['minecraft:gold_ingot']}).", ""]
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    areas = []
    for f in sorted(findings, key=lambda f: (order[f[0]], f[1])):
        if f[1] not in areas:
            areas.append(f[1])
    for area in areas:
        rows = sorted((f for f in findings if f[1] == area), key=lambda f: (order[f[0]], f[2]))
        out.append(f"== {area} ({len(rows)})")
        for level, _, where, msg in rows:
            out.append(f"  {level:<5} {where}")
            out.append(f"        {msg}")
        out.append("")
    p = summary["prices"]
    rockets = p.get("minecraft:firework_rocket")
    out.append("Reference prices (cheapest shop): " + ", ".join(
        f"{name(k)} {fmt(p[k])}" for k in ("ammo:tacz:9mm", "ammo:tacz:556x45", "ammo:tacz:12g", "ammo:tacz:50bmg")
        if k in p) + (f", rocket {fmt(rockets)}" if rockets else ""))
    counts = {lv: sum(1 for f in findings if f[0] == lv) for lv in order}
    out.append(f"{counts['ERROR']} error(s), {counts['WARN']} warning(s), {counts['INFO']} note(s).")
    text = "\n".join(out)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)
    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
