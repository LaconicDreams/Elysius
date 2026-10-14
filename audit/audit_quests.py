"""Quest audit (read only). Reads config/ftbquests/quests and the Paxi datapacks, writes only into audit/.

Usage: py audit/audit_quests.py      -> audit/QUEST_AUDIT.md, audit/quests.csv, audit/DELETE_CANDIDATES.md
Nothing outside audit/ is written. Categories and recommendations are rules in this file (CATEGORY_RULES,
CHAPTER_ADVICE, STORY_IDEAS); every number in the reports is counted from the quest files.
"""

import csv
import io
import os
import sys
from collections import Counter, defaultdict

AUDIT = os.path.dirname(os.path.abspath(__file__))
INST = os.path.dirname(AUDIT)
sys.path.insert(0, os.path.join(INST, "questtools"))

import gamedata  # noqa: E402
import snbt  # noqa: E402

QDIR = os.path.join(INST, "minecraft", "config", "ftbquests", "quests")
PAXI = os.path.join(INST, "minecraft", "config", "paxi", "datapacks")
RTYPES = ["Waffe", "Munition", "Aufsatz", "Raketen", "Shulker", "Sonstiges"]
UNUSED_AMMO_NOTE = "No gun uses this yet"     # subtitle the shop generator writes for calibres no gun fires

# ------------------------------------------------------------------ judgement (rules, not numbers)
CHAPTER_ADVICE = {
    "start_here": ("behalten", "Einziger Einstieg (Elytra, Raketen, Rucksack), die Story baut darauf auf."),
    "story_ashen_skyways": ("behalten", "Hauptstrang, hier sollen die großen Belohnungen hin."),
    "elytra_start": ("kürzen", "Einstiegskette ist gut, aber die 'Hard'-Bosse doppeln End Trophies / Long-Term und geben Waffen außerhalb der Story."),
    "good_deeds": ("kürzen", "16 Quests spiegeln nur Vanilla-Advancements 1:1 mit derselben Belohnungsart (Shulker); eine Auswahl plus Finale reicht."),
    "long_term": ("kürzen", "Stufenketten sind okay, aber Spielzeit-Quests sind Füller und die Boss-Kills passen besser in die Story."),
    "backpack_upgrades": ("behalten", "Jede Quest gibt ein eigenes, sonst knappes Upgrade, überschaubar."),
    "boss_dungeons": ("in die Story verschieben", "Laut Plan sind die Boss-Dungeons die Siegel des Hauptstrangs."),
    "horde_leaders": ("in die Story verschieben", "Eigene Mechanik des Packs; die Anführer eignen sich als Story-Gegner (z. B. Eintreiber des Boten)."),
    "overworld": ("zusammenlegen", "Vier kleine Bounty-Kapitel mit je 5 Quests lassen sich zu einem Kapitel 'Bounties' zusammenlegen."),
    "nether": ("zusammenlegen", "Wie Overworld: 5 Kill-Bounties, jede mit Waffe; gemeinsam mit den anderen Dimensionen."),
    "aether": ("zusammenlegen", "Wie Overworld; der Aether passt aber thematisch zum alten Pfad der Story."),
    "the_end": ("zusammenlegen", "Wie Overworld; doppelt End City und Drachen mit Taking Flight."),
    "gun_shop": ("später streichen", "53 Waffen gegen Erz untergraben Waffen als Story-Belohnung; erst nach fertiger Story streichen."),
    "rockets": ("kürzen", "Raketen sind für Elytra wichtig; Einzel- und Bulk-Version je Währung zusammenlegen."),
    "ammo_pistols_smgs": ("kürzen", "Einzel + Stack je Kaliber zusammenlegen, Kaliber ohne Waffe streichen."),
    "ammo_rifles": ("kürzen", "Einzel + Stack je Kaliber zusammenlegen, Kaliber ohne Waffe streichen."),
    "ammo_heavy": ("kürzen", "Einzel + Stack je Kaliber zusammenlegen."),
    "ammo_shotguns_launchers": ("kürzen", "Einzel + Stack je Kaliber zusammenlegen."),
    "att_sights": ("später streichen", "Aufsätze gibt es auch in Dungeon-Truhen; die 95 Aufsatz-Quests machen den Quest-Baum unübersichtlich."),
    "att_scopes": ("später streichen", "Siehe Sights."),
    "att_muzzles": ("später streichen", "Siehe Sights."),
    "att_grips": ("später streichen", "Siehe Sights."),
    "att_stocks": ("später streichen", "Siehe Sights."),
    "att_magazines": ("später streichen", "Siehe Sights."),
    "att_lasers": ("später streichen", "Siehe Sights."),
    "att_specials": ("später streichen", "Ammo-Mods (FMJ/HE/HP/I/Slug) sind stark und eher Story- oder Boss-Belohnungen."),
}

TUTORIAL_TITLES = {"Target Practice", "First Flight", "Night Sky Hunter", "Outpost Scout", "Welcome Aboard"}

# short suggestion for quests that hand out guns / attachments / big rewards outside the story
STORY_IDEAS = {
    "Target Practice": "Bleibt Tutorial; M1911 als Startwaffe ist okay, könnte aber Teil des modernen Pfads werden.",
    "Ghast Hunter": "AK-47 raus, stattdessen Story-Item (z. B. Ghast-Träne als Zutat für eine Bote-Aufgabe).",
    "Deep Dark Delve": "Ancient City als Story-Ort (alter Pfad); M700 als Belohnung dort statt in Taking Flight.",
    "Elder's Wrath": "Optionales Siegel oder Bote-Auftrag; goldene Äpfel als Nebenbelohnung lassen.",
    "Wither Sky": "Großer Story-Meilenstein (Nether-Kapitel des alten Pfads); Netherite dort vergeben.",
    "End City Raid": "Doppelt vorhanden (Taking Flight + End Trophies): eine davon streichen, die andere in die Story.",
    "Dragon Slayer": "Doppelt mit 'Dragon's End': Drachen als Story-Finale eines Akts, eine Quest streichen.",
    "Sky's the Limit": "Netherite-Brustplatte ist sehr groß für 'Elytra finden' (man startet mit Elytra); kleiner machen.",
    "Zombie Stopper": "Glock 17 als Belohnung des modernen Pfads (Kupfer/9mm) statt als Bounty.",
    "Web Cutter": "Bounty behalten, Waffe durch Munition/Raketen ersetzen.",
    "Creeper Crowd": "Bounty behalten, Waffe durch Munition/Raketen ersetzen.",
    "Raid Breaker": "Passt als Story-Schritt (Dorf verteidigen, Bote-Wunsch 'Macht'); MP5 dort vergeben.",
    "Beast Slayer": "Bounty behalten, Waffe durch Munition ersetzen.",
    "Blaze Runner": "AK-47 doppelt (auch Ghast Hunter): eine Vergabe streichen.",
    "Bone Crusher": "Wither-Skelette passen zum Ashen-Warlord-Siegel; AA-12 als Story-Belohnung dort.",
    "Hoglin Hunt": "M249 ist eine Emerald-Waffe: besser Story-Belohnung (Nether-Akt).",
    "Brute Force": "M700 doppelt (auch Deep Dark Delve): eine Vergabe streichen.",
    "Zephyr Chase": "Aether = alter Pfad der Story; Zephyr-Jagd als Story-Schritt, Waffe ggf. durch Aether-Item ersetzen.",
    "Stone Cold": "Wie Zephyr Chase.",
    "Sentry Shutdown": "M4A1 doppelt (auch Dragon Slayer): eine Vergabe streichen.",
    "Gatekeeper": "Slider ist ein Aether-Boss: guter Story-Meilenstein des alten Pfads.",
    "Enderman Ambush": "SCAR-H als End-Belohnung in die Story verschieben oder durch Munition ersetzen.",
    "Shell Game": "Bounty behalten, Waffe durch Munition/Shulker-Schalen ersetzen.",
    "Dragon's End": "Siehe Dragon Slayer.",
    "Sky Legend": "Minigun + 4 Netherite: als Story-Endbelohnung geeigneter als für Flugstrecke.",
    "Hunter III": "HK416D raus, Diamanten/Smaragde lassen.",
    "Hunter IV": "Golden Desert Eagle als Story-Trophäe (z. B. nach allen Siegeln).",
    "Deep Warden": "Warden als optionales Siegel; HE-Mod passt dorthin.",
    "Sun Spirit": "Aether-Endboss: Story-Meilenstein des alten Pfads.",
    "Valkyrie Queen": "Aether-Boss: Story-Meilenstein des alten Pfads.",
    "Monster Hunter": "Totem + 2 verzauberte Goldäpfel: als Long-Term okay, sonst Story-Finale.",
    "Pillar of the Community": "Totem + 16 Smaragde: okay als Nebenfinale, könnte Bote-Bezug bekommen ('gute Taten').",
    "Skyward Bound": "Netherite für Flugstrecke: okay, ggf. kleiner.",
    "Mansion Raider": "Waldanwesen als möglicher Story-Ort (Illager = 'Eintreiber'); sonst als Nebenquest okay.",
    "Sky Dweller": "Netherite nur für Spielzeit: Belohnung kleiner oder Quest streichen (Füller).",
    "Läufer": "Anführer als Bote-'Eintreiber' in die Story; Aufsatz als Belohnung passt.",
    "Brecher": "Wie Läufer.",
    "Spucker": "Wie Läufer.",
    "Schreier": "Wie Läufer.",
    "Kriecher": "Wie Läufer.",
    "Platzer": "Wie Läufer (gibt keinen Aufsatz, nur 40mm + Schießpulver).",
    "Leader Hunter": "HE-Mod + .50 BMG: guter Story-Meilenstein 'alle Eintreiber besiegt'.",
    "Ash to Ash": "Schon Siegel-Kandidat (Boss Dungeons).",
    "Eye of the Storm": "Schon Siegel-Kandidat (Boss Dungeons).",
    "Into the Hollow": "Schon Siegel-Kandidat (Boss Dungeons).",
}
BIG_ITEMS = {"minecraft:netherite_ingot", "minecraft:netherite_chestplate", "minecraft:totem_of_undying",
             "minecraft:enchanted_golden_apple", "minecraft:nether_star"}


def category(fn, q):
    t = q.get("title", "")
    tasks = q.get("tasks", [])
    if fn in ("story_ashen_skyways", "boss_dungeons"):
        return "Story"
    if is_shop(q):
        return "Shop"
    if q.get("can_repeat"):
        return "unklar (wiederholbar, aber kein reiner Item-Tausch)"
    if fn == "start_here" or (fn == "elytra_start" and t in TUTORIAL_TITLES):
        return "Tutorial/Einstieg"
    if fn == "elytra_start":
        return "Nebenquest" if q.get("optional") else "Meilenstein"
    if fn in ("overworld", "nether", "aether", "the_end"):
        return "Meilenstein" if all(x.get("type") == "dimension" for x in tasks) else "Nebenquest"
    if fn == "good_deeds":
        return "Meilenstein" if len(q.get("dependencies", [])) > 1 else "Nebenquest"
    if fn == "backpack_upgrades":
        return "Nebenquest"
    if fn == "horde_leaders":
        return "Meilenstein" if t in ("Cut Off the Head", "Leader Hunter") else "Nebenquest"
    if fn == "long_term":
        if any(x.get("stat") == "minecraft:play_time" for x in tasks):
            return "Füller"
        if all(x.get("type") == "structure" for x in tasks):
            return "Nebenquest"
        return "Meilenstein"
    return "unklar (keine Regel für dieses Kapitel)"


# ------------------------------------------------------------------ helpers
def is_shop(q):
    tasks, rewards = q.get("tasks", []), q.get("rewards", [])
    return bool(q.get("can_repeat") and tasks and rewards
                and all(t.get("type") == "item" and t.get("consume_items") for t in tasks)
                and all(r.get("type") == "item" for r in rewards))


def item_key(it):
    if isinstance(it, str):
        return it
    tag = it.get("tag") or {}
    for k in ("GunId", "AmmoId", "AttachmentId"):
        if k in tag:
            return f"{it['id']}#{tag[k]}"
    return it.get("id", "?")


def rtype(r):
    if r.get("type") != "item":
        return "Sonstiges"
    iid = item_key(r["item"]).split("#")[0]
    if iid == "tacz:modern_kinetic_gun":
        return "Waffe"
    if iid == "tacz:ammo":
        return "Munition"
    if iid == "tacz:attachment":
        return "Aufsatz"
    if iid == "minecraft:firework_rocket":
        return "Raketen"
    if iid.endswith("shulker_box"):
        return "Shulker"
    return "Sonstiges"


def rlabel(r):
    if r.get("type") == "command":
        return "Befehl: " + r.get("command", "")
    if r.get("type") != "item":
        return r.get("type", "?")
    k = item_key(r["item"])
    return f"{r.get('count', 1)}x {k.split('#')[-1]}"


def task_key(t):
    ty = t.get("type")
    tgt = t.get("advancement") or t.get("structure") or t.get("dimension") or t.get("entity") or t.get("stat")
    if ty == "item":
        tgt = item_key(t["item"])
    return ty, tgt


def task_label(t):
    ty, tgt = task_key(t)
    v = t.get("value")
    return f"{ty} {tgt}" + (f" ({v})" if v is not None else "") + (f" x{t.get('count')}" if t.get("count") else "")


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# ------------------------------------------------------------------ load
def load():
    groups = {g["id"]: g["title"] for g in snbt.load(os.path.join(QDIR, "chapter_groups.snbt"))["chapter_groups"]}
    chapters = []
    for f in sorted(os.listdir(os.path.join(QDIR, "chapters"))):
        if f.endswith(".snbt"):
            c = snbt.load(os.path.join(QDIR, "chapters", f))
            c["_file"] = f
            chapters.append(c)
    return groups, chapters


def datapack_advancements():
    found = set()
    for root, _, files in os.walk(PAXI):
        parts = root.replace("\\", "/").split("/")
        if "advancements" in parts:
            i = parts.index("advancements")
            ns = parts[i - 1]
            for f in files:
                if f.endswith(".json"):
                    found.add(f"{ns}:" + "/".join(parts[i + 1:] + [f[:-5]]))
    return found


def main():
    gd = gamedata.load()
    groups, chapters = load()
    dp_adv = datapack_advancements()
    all_ids = {}
    for c in chapters:
        for q in c["quests"]:
            all_ids[q["id"]] = (c, q)
    title_of = {i: cq[1].get("title", "") for i, cq in all_ids.items()}

    # ---------------- 1 inventory
    inv_rows, tot = [], Counter()
    for c in sorted(chapters, key=lambda c: (groups.get(c.get("group"), ""), c.get("order_index", 0))):
        qs = c["quests"]
        rc = Counter(rtype(r) for q in qs for r in q.get("rewards", []))
        rep = sum(1 for q in qs if q.get("can_repeat"))
        row = [c["_file"], c.get("title"), groups.get(c.get("group"), "?"), c.get("order_index"), len(qs), rep]
        row += [rc[k] for k in RTYPES]
        inv_rows.append(row)
        tot["quests"] += len(qs)
        tot["rep"] += rep
        for k in RTYPES:
            tot[k] += rc[k]
    total_row = ["**Summe**", f"{len(chapters)} Kapitel", "", "", tot["quests"], tot["rep"]] + [tot[k] for k in RTYPES]
    inv_rows.append(total_row)

    # ---------------- 2 categories
    cat = {q["id"]: category(c["filename"], q) for c in chapters for q in c["quests"]}
    cat_count = Counter(cat.values())
    cat_by_chapter = defaultdict(Counter)
    for c in chapters:
        for q in c["quests"]:
            cat_by_chapter[c["_file"]][cat[q["id"]]] += 1

    # ---------------- 4 shop analysis
    shops = [(c, q) for c in chapters for q in c["quests"] if is_shop(q)]
    shop_n = len(shops)
    shop_chapters = Counter(c["_file"] for c, q in shops)

    def okey(q):
        return tuple(sorted({item_key(r["item"]) for r in q["rewards"]}))

    def ikey(q):
        return tuple(sorted({item_key(t["item"]) for t in q["tasks"]}))

    merged = {}
    for c, q in shops:
        merged.setdefault((okey(q), ikey(q)), []).append((c, q))
    a_n = len(merged)
    unused_ammo = {k for k, v in merged.items() if any(UNUSED_AMMO_NOTE in q.get("subtitle", "") for _, q in v)}
    b_n = a_n - len(unused_ammo)

    def kind_of(k):
        return k[0][0].split("#")[0]

    gun_att = {k for k in merged if kind_of(k) in ("tacz:modern_kinetic_gun", "tacz:attachment")}
    c_n = b_n - len(gun_att - unused_ammo)
    shop_kind = Counter(kind_of(k) for k in merged)
    only_c = shop_n - sum(1 for c, q in shops if kind_of((okey(q),)) in ("tacz:modern_kinetic_gun", "tacz:attachment"))
    pct = lambda n: f"{100 * n / tot['quests']:.1f} %"  # noqa: E731

    # ---------------- 5 reward check
    big = []
    for c in chapters:
        if c["filename"] == "story_ashen_skyways":
            continue
        for q in c["quests"]:
            if is_shop(q):
                continue
            rts = {rtype(r) for r in q.get("rewards", [])}
            bigs = [rlabel(r) for r in q.get("rewards", [])
                    if r.get("type") == "item" and item_key(r["item"]) in BIG_ITEMS]
            if "Waffe" in rts or "Aufsatz" in rts or bigs:
                main_r = [rlabel(r) for r in q["rewards"] if rtype(r) in ("Waffe", "Aufsatz")] + bigs
                big.append([c["_file"], q.get("title"), ", ".join(main_r),
                            STORY_IDEAS.get(q.get("title", ""), "unklar (kein Vorschlag hinterlegt)")])

    # ---------------- 6 overlaps
    # same gun / attachment given by more than one one-off quest
    give = defaultdict(list)
    for c in chapters:
        for q in c["quests"]:
            if is_shop(q):
                continue
            for r in q.get("rewards", []):
                if rtype(r) in ("Waffe", "Aufsatz"):
                    give[item_key(r["item"]).split("#")[1]].append(f"{q.get('title')} ({c['filename']})")
    dup_rewards = [[k, len(v), "; ".join(v)] for k, v in sorted(give.items()) if len(v) > 1]
    # identical goals (same task type + target) in different one-off quests
    goals = defaultdict(list)
    for c in chapters:
        for q in c["quests"]:
            if is_shop(q):
                continue
            for t in q.get("tasks", []):
                ty, tgt = task_key(t)
                if ty in ("checkmark",):
                    continue
                goals[(ty, tgt)].append((q.get("title"), c["filename"], t.get("value"), len(q.get("tasks", []))))

    def rate(ty, v):
        if ty == "stat" and len({x[2] for x in v}) == len(v):
            return "Stufen (gewollt)"
        if len({x[1] for x in v}) == 1 and any(x[3] > 1 for x in v):
            return "Sammel-Quest (gewollt)"
        return "doppelt"

    dup_goals = [[f"{ty} {tgt}", len(v), rate(ty, v), "; ".join(
        f"{x[0]} ({x[1]}" + (f", {x[2]}" if x[2] is not None else "") + ")" for x in v)]
        for (ty, tgt), v in sorted(goals.items()) if len(v) > 1]
    real_dups = [r for r in dup_goals if r[2] == "doppelt"]
    nine_mm = sorted({q.get("title") for c in chapters for q in c["quests"] if not is_shop(q)
                      for r in q.get("rewards", []) if r.get("type") == "item"
                      and item_key(r["item"]) == "tacz:ammo#tacz:9mm"})
    # orphan dependencies, missing tasks/rewards, broken task targets, duplicate order_index per group
    orphans, no_task, no_reward, broken = [], [], [], []
    for c in chapters:
        for q in c["quests"]:
            for d in q.get("dependencies", []):
                if d not in all_ids:
                    orphans.append([c["_file"], q.get("title"), d])
            if not q.get("tasks"):
                no_task.append([c["_file"], q.get("title")])
            if not q.get("rewards"):
                no_reward.append([c["_file"], q.get("title")])
            for t in q.get("tasks", []):
                ty, tgt = task_key(t)
                ok = True
                if ty == "advancement":
                    ok = tgt in gd.advancements or tgt in dp_adv
                elif ty == "structure":
                    ok = tgt in gd.structures or tgt.startswith("#")
                elif ty == "dimension":
                    ok = tgt in gd.dimensions
                elif ty == "kill":
                    ok = tgt in gd.entities
                elif ty == "stat":
                    ok = tgt in gd.stats
                elif ty == "item":
                    ok = tgt.split("#")[0] in gd.items
                if not ok:
                    broken.append([c["_file"], q.get("title"), f"{ty} {tgt}"])
    order_dupes = []
    by_group = defaultdict(list)
    for c in chapters:
        by_group[groups.get(c.get("group"), "?")].append((c.get("order_index"), c["_file"]))
    for g, lst in by_group.items():
        cnt = Counter(o for o, _ in lst)
        for o, n in cnt.items():
            if n > 1:
                order_dupes.append([g, o, ", ".join(f for oo, f in lst if oo == o)])
    global_order = Counter(c.get("order_index") for c in chapters)
    # unreachable: a broken task, or a dependency chain that reaches an orphan / unreachable quest
    bad = {(r[0], r[1]) for r in broken}
    unreachable = set()
    changed = True
    while changed:
        changed = False
        for c in chapters:
            for q in c["quests"]:
                key = (c["_file"], q.get("title"))
                if key in unreachable:
                    continue
                deps = q.get("dependencies", [])
                if key in bad or any(d not in all_ids for d in deps) or any(
                        (all_ids[d][0]["_file"], all_ids[d][1].get("title")) in unreachable for d in deps if d in all_ids):
                    unreachable.add(key)
                    changed = True
    hidden_story = [q.get("title") for c in chapters for q in c["quests"]
                    if c["filename"] == "story_ashen_skyways"]

    # ---------------- 7 story links
    links = []
    for c in chapters:
        for q in c["quests"]:
            for r in q.get("rewards", []):
                if r.get("type") == "command":
                    links.append([c["_file"], q.get("title"), "Befehl-Belohnung", r.get("command")])
            for t in q.get("tasks", []):
                ty, tgt = task_key(t)
                ns = (tgt or "").split(":")[0]
                if ty in ("advancement", "structure") and ns in ("elytra_extras", "elytra_dungeons", "modpack"):
                    src = {"elytra_extras": "Datapack elytra_extras (Bote/Rezept)",
                           "elytra_dungeons": "Datapack elytra_dungeons (Boss-Dungeons)",
                           "modpack": "Datapack elytra_hordes (Horde Leaders)"}[ns]
                    links.append([c["_file"], q.get("title"), f"Aufgabe {ty}", f"{tgt} -> {src}"])
    used_adv = {task_key(t)[1] for c in chapters for q in c["quests"] for t in q.get("tasks", [])
                if t.get("type") == "advancement"}
    unused_dp_adv = sorted(a for a in dp_adv if a not in used_adv and not a.endswith("/root"))

    # ---------------- recommendations per quest (CSV)
    bulk_titles = {q["id"] for c, q in shops}
    single_of = {}
    for k, v in merged.items():
        if len(v) > 1:
            for _, q in v:
                single_of[q["id"]] = len(v)

    def quest_advice(c, q):
        base = CHAPTER_ADVICE.get(c["filename"], ("unklar", ""))[0]
        if UNUSED_AMMO_NOTE in q.get("subtitle", ""):
            return "später streichen (keine Waffe nutzt dieses Kaliber)"
        if q["id"] in single_of and q["id"] in bulk_titles:
            return f"{base}; Einzel+Stack zusammenlegen"
        if c["filename"] in ("elytra_start", "the_end") and q.get("title") in ("End City Raid", "Dragon Slayer", "Dragon's End"):
            return f"{base}; doppeltes Ziel"
        return base

    csv_rows = []
    for c in chapters:
        for q in c["quests"]:
            rts = Counter(rtype(r) for r in q.get("rewards", []))
            csv_rows.append([c["_file"], q["id"], q.get("title", ""), cat[q["id"]],
                             "ja" if q.get("can_repeat") else "nein",
                             "+".join(k for k in RTYPES if rts[k]) or "keine",
                             " ".join(f"{d} ({title_of.get(d, 'FEHLT')})" for d in q.get("dependencies", [])),
                             quest_advice(c, q)])

    # ---------------- write CSV
    with open(os.path.join(AUDIT, "quests.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Kapitel-Datei", "Quest-ID", "Titel", "Kategorie", "wiederholbar", "Belohnungsart",
                    "Abhängigkeiten", "Empfehlung"])
        w.writerows(csv_rows)

    # ---------------- write report
    ammo_unused = sorted(k[0][0].split("#")[1] for k in unused_ammo)
    nonshop = tot["quests"] - shop_n
    o = io.StringIO()
    p = lambda *a: print(*a, file=o)  # noqa: E731
    p("# Quest-Audit Elysius (nur gelesen, nichts geändert)\n")
    p(f"Stand: Dateien in `minecraft/config/ftbquests/quests`, erzeugt von `audit/audit_quests.py`.\n")
    p("## Zusammenfassung")
    p(f"- {len(chapters)} Kapitel, **{tot['quests']} Quests**, davon {tot['rep']} wiederholbar.")
    p(f"- **{shop_n} Shop-Quests = {pct(shop_n)}** aller Quests; nur {nonshop} Quests sind keine Shop-Einträge.")
    p(f"- Shop schrumpft auf {a_n} (Einzel+Stack zusammen), {b_n} (+ Kaliber ohne Waffe raus), "
      f"{c_n} (+ Waffen und Aufsätze raus).")
    p(f"- Story hat erst {cat_count['Story']} Quests (3 'Zwischen den Zeiten' + 3 Boss-Dungeons).")
    p(f"- {len(big)} Nicht-Story-Quests geben Waffen, Aufsätze oder große Belohnungen (Abschnitt 5).")
    p(f"- {len(dup_rewards)} Waffen/Aufsätze werden von mehreren Quests verschenkt; {len(real_dups)} Ziele sind echt doppelt "
      f"(z. B. End City, Enderdrache, Nether/End betreten).")
    p(f"- {len(ammo_unused)} Munitionssorten im Shop haben keine Waffe ({', '.join(ammo_unused)}).")
    p(f"- Verwaiste Abhängigkeiten: {len(orphans)}, Quests ohne Aufgabe: {len(no_task)}, ohne Belohnung: {len(no_reward)}, "
      f"kaputte Aufgabenziele: {len(broken)}.")
    p(f"- order_index doppelt innerhalb einer Gruppe: {len(order_dupes)}.")
    p("- Alle Kapitel werden von `questtools/questgen.py` erzeugt: Streichungen später dort machen, nicht in den .snbt.")
    p("")
    p("## 1. Inventar")
    p("Belohnungen = Anzahl Belohnungs-Einträge in den Dateien (große Munitionsmengen sind oft auf 2 bis 4 Einträge verteilt).\n")
    p(md_table(["Datei", "Titel", "Gruppe", "order", "Quests", "wiederholbar"] + RTYPES, inv_rows))
    p("")
    p("## 2. Kategorien")
    p(md_table(["Kategorie", "Quests"], sorted(cat_count.items(), key=lambda x: -x[1])))
    p("")
    p("Regeln: Story = 'Zwischen den Zeiten' + Boss Dungeons. Shop = wiederholbar, verbraucht nur Items, gibt nur Items. "
      "Tutorial = Start Here + die erste Kette in Taking Flight. Meilenstein = Dimension betreten, Boss/Vanilla-Boss, "
      "Stufen (Flugstrecke, Kills), Finale. Nebenquest = Kill-Bounties, Good Deeds, Rucksack-Upgrades, einzelne Anführer, "
      "Strukturen. Füller = Spielzeit-Quests (verlangen keine Handlung). Pro Quest: `quests.csv`.\n")
    rows = [[f, ", ".join(f"{k}: {n}" for k, n in cc.most_common())] for f, cc in sorted(cat_by_chapter.items())]
    p(md_table(["Kapitel", "Kategorien"], rows))
    p("")
    p("## 3. Empfehlung je Kapitel")
    p(md_table(["Kapitel", "Empfehlung", "Grund"],
               [[c["_file"], *CHAPTER_ADVICE.get(c["filename"], ("unklar", "keine Regel"))] for c in
                sorted(chapters, key=lambda c: (groups.get(c.get("group"), ""), c.get("order_index", 0)))]))
    p("")
    p("Auffällige Einzelfälle: siehe Abschnitt 5 und 6 sowie `DELETE_CANDIDATES.md`.\n")
    p("## 4. Shop-Analyse")
    p(f"- Shop-Quests: **{shop_n} von {tot['quests']} ({pct(shop_n)})**.")
    p("- Kapitel: " + ", ".join(f"{f} ({n})" for f, n in sorted(shop_chapters.items())) + ".")
    p("")
    p(md_table(["Schritt (aufeinander aufbauend)", "Shop-Quests", "Anteil an heutiger Gesamtzahl", "Quests gesamt danach"], [
        ["heute", shop_n, pct(shop_n), tot["quests"]],
        ["(a) Einzel + Stack je Item/Währung zu einer Quest", a_n, pct(a_n), nonshop + a_n],
        ["(b) Munition: 1 Quest pro Kaliber, Kaliber ohne Waffe gestrichen", b_n, pct(b_n), nonshop + b_n],
        ["(c) zusätzlich Waffen und Aufsätze ganz entfernt", c_n, pct(c_n), nonshop + c_n],
    ]))
    p("")
    p(f"- Nach (a) bleiben je Art: " + ", ".join(f"{k.split(':')[1]}: {n}" for k, n in shop_kind.most_common()) + ".")
    p(f"- Nur (c) ohne (a)/(b): {only_c} Shop-Quests (Waffen und Aufsätze raus, Munition/Raketen unverändert).")
    p("- (b) erklärt: nach (a) gibt es schon genau 1 Quest pro Kaliber; 'wenige' heißt hier zusätzlich: Kaliber, die laut "
      f"Untertitel keine Waffe nutzt, fallen weg ({len(ammo_unused)}).")
    p("")
    p("## 5. Belohnungs-Check (Waffen, Aufsätze, große Belohnungen außerhalb der Story)")
    p(md_table(["Kapitel", "Quest", "Belohnung", "Vorschlag"], big))
    p("")
    p("## 6. Überschneidungen")
    p("### Gleiche Waffe/Aufsatz von mehreren Quests (ohne Shop)")
    p(md_table(["Item", "Anzahl", "Quests"], dup_rewards) if dup_rewards else "Keine.")
    p("\nZusätzlich ist **jede** als Quest-Belohnung vergebene Waffe auch im Gun Shop kaufbar.\n")
    p("### Gleiches Ziel (gleicher Aufgabentyp + Ziel, ohne Shop)")
    p("Bei `stat` steht der Zielwert dabei; unterschiedliche Werte sind Stufen, keine echten Doppelungen.\n")
    p(md_table(["Ziel", "Anzahl", "Bewertung", "Quests"], dup_goals))
    p("")
    p("### Technische Prüfungen")
    p(f"- Verwaiste Abhängigkeiten (ID existiert nicht): {len(orphans)}" + (
        "\n" + md_table(["Kapitel", "Quest", "fehlende ID"], orphans) if orphans else ""))
    p(f"- Quests ohne Aufgabe: {len(no_task)}" + (": " + ", ".join(f"{a}/{b}" for a, b in no_task) if no_task else ""))
    p(f"- Quests ohne Belohnung: {len(no_reward)}" + (": " + ", ".join(f"{a}/{b}" for a, b in no_reward) if no_reward else ""))
    p(f"- Aufgaben mit unbekanntem Ziel (Advancement/Struktur/Dimension/Mob/Stat/Item nicht gefunden): {len(broken)}" + (
        "\n" + md_table(["Kapitel", "Quest", "Ziel"], broken) if broken else ""))
    p(f"- Unerreichbare Quests (kaputtes Ziel oder Abhängigkeit darauf): {len(unreachable)}" + (
        ": " + ", ".join(f"{a}/{b}" for a, b in sorted(unreachable)) if unreachable else ""))
    p(f"- order_index doppelt innerhalb einer Gruppe: {len(order_dupes)}" + (
        "\n" + md_table(["Gruppe", "order", "Kapitel"], order_dupes) if order_dupes else ""))
    p("- order_index über Gruppen hinweg gleich (normal, FTB sortiert pro Gruppe): "
      + ", ".join(f"{o}: {n}x" for o, n in sorted(global_order.items()) if n > 1) + ".")
    p("- Nicht prüfbar ohne Spiel: ob 'Long Haul' (Taking Flight) ohne Abhängigkeit absichtlich frei ist; ob die "
      "Story-Quests im Spiel wirklich unsichtbar bleiben (Kapitel-Flag `hide_quest_until_deps_complete`).")
    p("")
    p("## 7. Verbindungen Quests <-> Bote / Boss-Dungeons / Horde Leaders")
    p(md_table(["Kapitel", "Quest", "Art", "Ziel / Quelle"], links))
    p("")
    p("Weitere Verbindungen (nicht in Quest-Dateien, aber relevant beim Streichen):")
    p("- Boss-Advancements werden von `elytra_dungeons/.../victory.mcfunction` per `advancement grant @a[distance=..48/64]` vergeben.")
    p("- Horde-Leader-Advancements (`modpack:leaders/*`) lösen beim Töten eines Mobs mit Tag `modpack_horde_leader` aus.")
    p("- Bote-Wunsch 'Macht' (Fehlschlag) startet eine Horde über `modpack:horde/start` (Datapack-zu-Datapack, keine Quest).")
    p("- Rezept 'Kackhaufen' (Story Q3) braucht 1 Patrone 9mm; Q2 'Kupferpfeil' gibt genau 1 Patrone. Weitere 9mm-Quellen in "
      f"Quests: Shop '9mm Ammo' und {', '.join(nine_mm)}. Fällt der Shop weg, bleibt Q2 die sichere Quelle.")
    p("- Datapack-Advancements, die noch keine Quest nutzt: " + ", ".join(f"`{a}`" for a in unused_dp_adv) + ".")
    with open(os.path.join(AUDIT, "QUEST_AUDIT.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(o.getvalue())

    # ---------------- delete candidates
    o = io.StringIO()
    p("# Streich-Kandidaten (nur eine Liste, es wird nichts gelöscht)\n")
    p("Reihenfolge = Vorschlag, wann. Alles erst, wenn die Story steht (der Shop bleibt bis dahin).")
    p("Umsetzen später in `questtools/questgen.py`, nicht direkt in den .snbt-Dateien.\n")
    p("## Sofort unkritisch (kein Spielwert)")
    rows = [[c["_file"], q.get("title"), q["id"], "Munition ohne passende Waffe (Untertitel: 'No gun uses this yet')"]
            for c, q in shops if UNUSED_AMMO_NOTE in q.get("subtitle", "")]
    p(md_table(["Kapitel", "Quest", "ID", "Grund"], rows))
    p("")
    p("## Doppelte Ziele (eine von zwei behalten)")
    rows = []
    for c in chapters:
        for q in c["quests"]:
            if c["filename"] == "elytra_start" and q.get("title") in ("End City Raid", "Dragon Slayer", "Into the End",
                                                                     "Nether Glider"):
                twin = {"End City Raid": "End Trophies 'End City Raid'", "Dragon Slayer": "End Trophies 'Dragon's End'",
                        "Into the End": "End Trophies 'The Final Frontier' + Backpack 'Always Stocked'",
                        "Nether Glider": "Nether 'Through the Portal' + Backpack 'Hot Pocket'"}[q.get("title")]
                rows.append([c["_file"], q.get("title"), q["id"], f"Gleiches Ziel wie {twin}"])
    p(md_table(["Kapitel", "Quest", "ID", "Grund"], rows))
    p("")
    p("## Zusammenlegen statt streichen (Shop, Schritt a)")
    rows = []
    for (ok, ik), v in sorted(merged.items(), key=lambda kv: kv[1][0][0]["_file"]):
        if len(v) > 1:
            rows.append([v[0][0]["_file"], " + ".join(q.get("title") for _, q in v), f"{len(v)} -> 1"])
    p(md_table(["Kapitel", "Quests", "Wirkung"], rows))
    p("")
    p("## Später streichen (nach fertiger Story)")
    rows = [[c["_file"], c.get("title"), len(c["quests"]), CHAPTER_ADVICE[c["filename"]][1]]
            for c in chapters if CHAPTER_ADVICE.get(c["filename"], ("",))[0] == "später streichen"]
    p(md_table(["Kapitel", "Titel", "Quests", "Grund"], rows))
    p(f"\nSumme dieser Kapitel: {sum(r[2] for r in rows)} Quests.\n")
    p("## Füller")
    rows = [[c["_file"], q.get("title"), q["id"], "Spielzeit-Quest, verlangt keine Handlung"]
            for c in chapters for q in c["quests"] if cat[q["id"]] == "Füller"]
    p(md_table(["Kapitel", "Quest", "ID", "Grund"], rows))
    p("")
    p("## Kürzen (Auswahl behalten)")
    gd_ch = next(c for c in chapters if c["filename"] == "good_deeds")
    finale = next(q for q in gd_ch["quests"] if len(q.get("dependencies", [])) > 1)
    outside = [q.get("title") for q in gd_ch["quests"] if q is not finale and q["id"] not in finale["dependencies"]]
    p(f"- `good_deeds.snbt`: {len(gd_ch['quests']) - 1} Vanilla-Advancement-Spiegel mit je einer Shulker-Kiste. Vorschlag: "
      f"die {len(finale['dependencies'])} Voraussetzungen des Finales '{finale.get('title')}' behalten, die "
      f"{len(outside)} anderen streichen: {', '.join(outside)}.")
    with open(os.path.join(AUDIT, "DELETE_CANDIDATES.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(o.getvalue())

    print(f"chapters={len(chapters)} quests={tot['quests']} repeat={tot['rep']} shop={shop_n} a={a_n} b={b_n} c={c_n} "
          f"only_c={only_c} big={len(big)} dup_rewards={len(dup_rewards)} dup_goals={len(dup_goals)} orphans={len(orphans)} "
          f"broken={len(broken)} unreachable={len(unreachable)} order_dupes={len(order_dupes)}")
    print("rewards", {k: tot[k] for k in RTYPES}, "categories", dict(cat_count))


if __name__ == "__main__":
    main()
