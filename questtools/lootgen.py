"""
Chest loot generator: adds TaCZ guns, attachments and ammo to structure chests.
==============================================================================
Nothing is removed from any chest. The output is a small TaCZ gun pack (minecraft/tacz/elytra_loot)
whose loot injectors add extra pools on top of each chest's normal loot.

    py lootgen.py           write the pack and loot_report.txt
    py lootgen.py --check   only print the report

Every chest loot table found in the installed mods is put in a tier (1 = easy, 5 = hardest) by
tier_of() below, or left out (None). Which guns, attachments and ammo a tier can roll, and how often,
comes from the tables under TUNING. Prices are read from the shop chapters, so a gun that costs more
in the shop is rarer in chests. Rerun this after changing shop prices.
"""

import json
import math
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import balance  # noqa: E402
import gamedata  # noqa: E402

PACK_NS = "elytra_loot"
PACK_DIR = os.path.join(gamedata.MC_DIR, "tacz", PACK_NS)
REPORT = os.path.join(HERE, "loot_report.txt")

# =================================================================== TUNING
# Chance that a chest of this tier contains a gun / an attachment / ammo (ammo can roll more than once).
CHANCE = {
    #     gun    attachment  ammo   ammo rolls
    1: (0.03,  0.06,       0.15,  (1, 1)),
    2: (0.08,  0.15,       0.30,  (1, 1)),
    3: (0.15,  0.25,       0.45,  (1, 1)),
    4: (0.25,  0.35,       0.60,  (1, 2)),
    5: (0.26,  0.45,       0.75,  (2, 2)),   # + the top guns below
}
# Which guns a tier can roll, by shop price in iron (diamond = 8, emerald = 6), and how strongly the
# cheaper guns are favoured (weight = price ** bias; -1 = cheap guns much more common, 0 = all equal).
GUN_RANGE = {1: (0, 24, -1.0), 2: (0, 48, -1.0), 3: (20, 112, -1.0), 4: (56, 216, -0.5), 5: (96, 216, 0.0)}
# The strongest guns only drop in tier 5, each with this chance per chest.
TOP_GUNS = ["m95", "m107", "minigun", "ai_awp", "taurus500", "fn_evolys"]
TOP_GUN_CHANCE = 0.015
# Guns that are not sold in the shop still need a price to be placed in a tier.
UNSOLD_GUN_PRICE = {"tacz:taurus943": 16}
# Attachments: max shop price in iron per tier and bias (positive = pricier ones favoured).
ATT_RANGE = {1: (8, -1.0), 2: (16, -1.0), 3: (32, -0.5), 4: (80, 0.0), 5: (10 ** 9, 0.5)}
# Ammo: how much of one stack a roll gives, and how the calibre families are weighted per tier.
AMMO_STACK_SHARE = {1: (0.15, 0.35), 2: (0.2, 0.45), 3: (0.3, 0.6), 4: (0.4, 0.8), 5: (0.5, 1.0)}
AMMO_FAMILY_WEIGHT = {
    #     pistol  rifle  shotgun  heavy  explosive
    1: (6,      2,     1,       0.5,   0),
    2: (4,      4,     1.5,     1,     0),
    3: (3,      5,     1.5,     2,     0.5),
    4: (2,      5,     1.5,     3,     1),
    5: (1,      4,     1,       4,     1.5),
}
FAMILY_OF_CHAPTER = {"ammo_pistols_smgs": 0, "ammo_rifles": 1, "ammo_heavy": 3}
EXPLOSIVES = {"tacz:40mm", "tacz:rpg_rocket"}

# Dungeons Arise structures by difficulty. Their treasure chests get this tier, other chests one less.
DA_TIER = {
    5: ["heavenly_conqueror", "heavenly_challenger", "heavenly_rider", "typhon", "ceryneian_hind"],
    4: ["keep_kayra", "shiraz_palace", "plague_asylum", "mechanical_nest", "foundry", "scorched_mines",
        "infested_temple", "thornborn_towers", "illager_fort", "illager_corsair", "illager_galley",
        "undead_pirate_ship", "mining_system"],
    3: ["bandit_towers", "aviary", "monastery", "illager_windmill", "jungle_tree_house", "mushroom_mines",
        "abandoned_temple", "small_blimp"],
    2: ["bandit_village", "illager_campsite", "mushroom_house", "mushroom_village", "giant_mushroom",
        "lighthouse", "greenwood_pub", "bathhouse", "small_prairie_house", "fishing_hut"],
}

# Containers that never get anything: storage barrels, food, maps, decorations, trash, special boxes.
EXCLUDE = re.compile(r"barrel|food_storage|_map$|/map$|tent$|gummies|_disc$|trash|cape_config|ice_box|"
                     r"spawner_box|magma_box|potions|dispenser|spawn_bonus_chest|trader_elephant|lucky_pool|"
                     r"coal_storage|/pot$|wardrobe|merchant_campsite|enchants$|bookshelf")


def tier_of(table):
    """Loot table id -> tier 1-5, or None to leave it alone."""
    ns, path = table.split(":", 1)
    if EXCLUDE.search(path):
        return None
    name = path.split("/")[-1]

    if ns == "minecraft":
        if path.startswith("chests/village/"):
            return 1 if re.search(r"weaponsmith|armorer|toolsmith|fletcher", path) else None
        table_tiers = {
            5: ["end_city_treasure"],
            4: ["bastion_treasure", "ancient_city"],
            3: ["nether_bridge", "bastion_other", "bastion_bridge", "bastion_hoglin_stable", "woodland_mansion",
                "stronghold_library"],
            2: ["simple_dungeon", "desert_pyramid", "jungle_temple", "shipwreck_treasure", "stronghold_corridor",
                "stronghold_crossing", "pillager_outpost", "buried_treasure"],
            1: ["abandoned_mineshaft", "igloo_chest", "ruined_portal", "shipwreck_supply", "underwater_ruin_big",
                "underwater_ruin_small"],
        }
        for t, names in table_tiers.items():
            if name in names:
                return t
        return None

    if ns == "aether":
        if "gold_dungeon" in path:
            return 5
        if "silver_dungeon" in path:
            return 4 if re.search(r"reward|treasure|valkyrie|gravitite", name) else 3
        if "bronze_dungeon" in path:
            return 3 if re.search(r"reward|treasure|neptune", name) else 2
        if name == "ruined_portal":
            return 1
        return None

    if ns == "dungeons_arise":
        m = re.match(r"chests/mines_treasure_(small|medium|big)$", path)
        if m:
            return {"small": 1, "medium": 2, "big": 3}[m.group(1)]
        struct = path.split("/")[1] if path.count("/") >= 2 else name
        for t, structs in DA_TIER.items():
            if struct in structs:
                treasure = re.search(r"treasure|elite|_reward", name)
                return t if treasure else max(1, t - 1)
        return None

    if ns == "repurposed_structures":
        if path.startswith("chests/villages/"):
            return 1 if "weaponsmith" in path else None
        if re.search(r"/end|ancient_cities|bastions/underground/treasure", path):
            return 4
        if re.search(r"nether|crimson|warped|basalt|soul|bastions|mansions|fortresses|cities/|monuments/", path):
            return 3
        if re.search(r"dungeons/|pyramids/|temples/|outposts/|ruins/land_\w+/large|shipwrecks/.*/treasure", path):
            return 2
        if re.search(r"mineshafts/|igloos/|ruins/|shipwrecks/|ruined_portals/", path):
            return 1
        return None

    if ns == "betterstrongholds":
        return 4 if re.search(r"treasure|armoury|cmd_yung", name) else 3
    if ns == "betterfortresses":
        return 4 if name in ("keep", "beacon", "obsidian") else 3
    if ns == "betterdeserttemples":
        return 4 if name in ("tomb_pharaoh", "pharaoh_hidden") else 2
    if ns == "betterjungletemples":
        return 2 if name == "treasure" else 1
    if ns == "betteroceanmonuments":
        return 3
    if ns == "betterdungeons":
        if path.startswith("small_dungeon"):
            return 1
        return 3 if "nether" in path else 2
    if ns == "terralith":
        return 1
    return None


# =================================================================== engine

def chest_tables():
    """Every chest-like loot table in the client jar and the mods."""
    found = set()
    for kind, p in gamedata._sources():
        if os.path.isdir(p):
            continue
        try:
            z = zipfile.ZipFile(p)
        except (OSError, zipfile.BadZipFile):
            continue
        with z:
            for n in z.namelist():
                m = re.match(r"data/([^/]+)/loot_tables/(.+)\.json$", n)
                if m and re.search(r"chest", m.group(2)) and not m.group(2).startswith(("entities/", "blocks/")):
                    found.add(f"{m.group(1)}:{m.group(2)}")
    return sorted(found)


def nbt_str(d):
    parts = []
    for k, v in d.items():
        parts.append(f"{k}:{json.dumps(v) if isinstance(v, str) else v}")
    return "{" + ",".join(parts) + "}"


def item(item_id, tag, count=None, weight=None):
    e = {"type": "minecraft:item", "name": item_id, "functions": [{"function": "minecraft:set_nbt", "tag": nbt_str(tag)}]}
    if count:
        lo, hi = count
        e["functions"].append({"function": "minecraft:set_count",
                               "count": lo if lo == hi else {"type": "minecraft:uniform", "min": lo, "max": hi}})
    if weight is not None:
        e["weight"] = max(1, int(round(weight)))
    return e


def chance_pool(chance, entries, rolls=(1, 1)):
    pool = {"rolls": rolls[0] if rolls[0] == rolls[1] else {"type": "minecraft:uniform", "min": rolls[0], "max": rolls[1]},
            "entries": entries}
    if chance < 1:
        pool["conditions"] = [{"condition": "minecraft:random_chance", "chance": round(chance, 5)}]
    return pool


class Economy:
    def __init__(self):
        gd = gamedata.load()
        _, summary, _ = balance.audit()
        prices = summary["prices"]
        self.gd = gd
        self.guns = {}
        for k, v in prices.items():
            if k.startswith("gun:"):
                self.guns[k[4:]] = v
        for gid, v in UNSOLD_GUN_PRICE.items():
            self.guns.setdefault(gid, v)
        self.atts = {k[4:]: v for k, v in prices.items() if k.startswith("att:")}
        # ammo families from the shop chapter each calibre is sold in
        self.ammo = {}
        valuer_shops = {}
        chapters_dir = os.path.join(gamedata.QUESTS_DIR, "chapters")
        import snbt
        for f in os.listdir(chapters_dir):
            if f.startswith("ammo_") and f.endswith(".snbt"):
                for q in snbt.load(os.path.join(chapters_dir, f))["quests"]:
                    for r in q.get("rewards", []):
                        it = r.get("item")
                        if isinstance(it, dict) and it.get("id") == "tacz:ammo":
                            valuer_shops[it["tag"]["AmmoId"]] = f[:-5]
        for aid, chapter in valuer_shops.items():
            if not gd.guns_using(aid):
                continue  # nobody can fire it
            fam = FAMILY_OF_CHAPTER.get(chapter, 2)
            if aid in EXPLOSIVES:
                fam = 4
            self.ammo[aid] = fam

    def gun_name(self, gid):
        return self.gd.tacz_name("gun", gid) or gid

    def ammo_for_gun(self, gid):
        aid = self.gd.gun_ammo(gid)
        stack = self.gd.ammo_stack(aid)
        mag = self.gd.gun_mag(gid) or max(1, stack // 2)
        lo = max(mag, math.ceil(stack / 6))
        hi = min(stack, max(2 * mag, math.ceil(stack / 3)))
        return aid, (min(lo, hi), hi)


def build_tier(t, eco):
    gd = eco.gd
    p_gun, p_att, p_ammo, ammo_rolls = CHANCE[t]
    pools, report = [], []
    top = {f"tacz:{g}" for g in TOP_GUNS}

    # guns: one pool per gun so the gun and its ammo always drop together
    lo, hi, bias = GUN_RANGE[t]
    eligible = {g: p for g, p in eco.guns.items() if lo <= p <= hi and g not in top and g in gd.guns}
    weights = {g: p ** bias for g, p in eligible.items()}
    total = sum(weights.values()) or 1
    gun_chances = {g: p_gun * w / total for g, w in weights.items()}
    if t == 5:
        for g in top:
            if g in gd.guns:
                gun_chances[g] = TOP_GUN_CHANCE
    for g, c in sorted(gun_chances.items(), key=lambda x: -x[1]):
        modes = gd.gun_modes(g)
        tag = {"GunId": g, "GunFireMode": modes[0] if modes else "SEMI", "GunCurrentAmmoCount": 0}
        aid, cnt = eco.ammo_for_gun(g)
        children = [item("tacz:modern_kinetic_gun", tag)]
        if aid:
            children.append(item("tacz:ammo", {"AmmoId": aid}, cnt))
        pools.append(chance_pool(c, [{"type": "minecraft:group", "children": children}]))
        report.append(f"    {c * 100:5.2f}%  {eco.gun_name(g)}  (+{cnt[0]}-{cnt[1]} rounds)")

    # attachments: one weighted pool
    cap, abias = ATT_RANGE[t]
    atts = {a: p for a, p in eco.atts.items() if p <= cap and a in gd.attachments}
    if atts:
        aw = {a: p ** abias for a, p in atts.items()}
        scale = 1000 / max(aw.values())
        pools.append(chance_pool(p_att, [item("tacz:attachment", {"AttachmentId": a}, weight=w * scale)
                                         for a, w in sorted(aw.items())]))

    # ammo: one weighted pool over every calibre someone can fire
    fam_w = AMMO_FAMILY_WEIGHT[t]
    share = AMMO_STACK_SHARE[t]
    fam_size = {}
    for aid, fam in eco.ammo.items():
        fam_size[fam] = fam_size.get(fam, 0) + len(gd.guns_using(aid))
    entries, ammo_lines = [], []
    for aid, fam in sorted(eco.ammo.items()):
        w = fam_w[fam] * len(gd.guns_using(aid)) / fam_size[fam]
        if w <= 0:
            continue
        stack = gd.ammo_stack(aid)
        cnt = (max(1, round(stack * share[0])), max(1, round(stack * share[1])))
        entries.append(item("tacz:ammo", {"AmmoId": aid}, cnt, weight=w * 1000))
        ammo_lines.append((w, f"{aid.split(':')[1]} {cnt[0]}-{cnt[1]}"))
    pools.append(chance_pool(p_ammo, entries, ammo_rolls))

    total_gun = 1 - math.prod(1 - c for c in gun_chances.values())
    head = [f"  gun {total_gun * 100:.0f}% | attachment {p_att * 100:.0f}% ({len(atts)} kinds, up to {cap if cap < 1e6 else 'any'} iron) | "
            f"ammo {p_ammo * 100:.0f}% x{ammo_rolls[0]}-{ammo_rolls[1]} rolls"]
    tw = sum(w for w, _ in ammo_lines)
    head.append("  ammo mix: " + ", ".join(f"{s} ({w / tw * 100:.0f}%)" for w, s in sorted(ammo_lines, reverse=True)[:8])
                + (" ..." if len(ammo_lines) > 8 else ""))
    head.append("  guns (chance per chest):")
    return pools, head + report


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check = "--check" in argv
    eco = Economy()
    tables = chest_tables()
    by_tier = {t: [] for t in range(1, 6)}
    skipped = []
    for tb in tables:
        t = tier_of(tb)
        (by_tier[t] if t else skipped).append(tb)

    lines = ["Chest loot added by questtools/lootgen.py (original chest loot is untouched)", ""]
    files = {}
    for t in range(1, 6):
        pools, rep = build_tier(t, eco)
        files[f"tier{t}.json"] = {"loot_tables": by_tier[t], "pools": pools}
        lines.append(f"TIER {t}: {len(by_tier[t])} chest types")
        lines.extend(rep)
        lines.append("")
    for t in range(1, 6):
        lines.append(f"TIER {t} chests:")
        lines.extend(f"  {x}" for x in by_tier[t])
        lines.append("")
    lines.append(f"NOT CHANGED ({len(skipped)}): storage barrels, villages, maps, food, special boxes:")
    lines.extend(f"  {x}" for x in skipped)
    text = "\n".join(lines) + "\n"

    print("\n".join(lines[: lines.index("TIER 1 chests:")]))
    print(f"{sum(len(v) for v in by_tier.values())} chest types get loot, {len(skipped)} left alone. "
          f"Full list in {os.path.relpath(REPORT, gamedata.INSTANCE)}")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(text)
    if check:
        return 0

    inj = os.path.join(PACK_DIR, "data", PACK_NS, "tacz_loot_injectors")
    os.makedirs(inj, exist_ok=True)
    os.makedirs(os.path.join(PACK_DIR, "assets", PACK_NS), exist_ok=True)
    with open(os.path.join(PACK_DIR, "gunpack.meta.json"), "w", encoding="utf-8") as f:
        json.dump({"namespace": PACK_NS}, f, indent=2)
    with open(os.path.join(PACK_DIR, "assets", PACK_NS, "gunpack_info.json"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0.0", "name": "Elytra modpack chest loot",
                   "desc": "Adds guns, attachments and ammo to structure chests. Generated by questtools/lootgen.py",
                   "license": "All Rights Reserved", "authors": ["Elytra modpack"], "date": "2026-10-08"}, f, indent=2)
    for old in os.listdir(inj):
        if old.endswith(".json") and old not in files:
            os.remove(os.path.join(inj, old))
    for name, data in files.items():
        with open(os.path.join(inj, name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1)
    print(f"Wrote {len(files)} injector files to minecraft/tacz/{PACK_NS}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
