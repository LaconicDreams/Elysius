"""
Pfad-Belohnungen (Macht / Schutz / Wissen)  ->  elytra_extras: data/modpack/functions/bote/pfad/,
                                                 data/aether/loot_tables/... (overrides without the path items)
=====================================================================================================
Each wish path gets its own Aether items as quest items (unbreakable, lore "Gabe des Boten" + path, NBT tags
modpack_questitem:1b, modpack_pfad:"<pfad>", modpack_teil:"<teil>"; item names unchanged).
  * first weapon right after the wish is chosen, armour piece by piece with the rank, endgame weapon at rank 7
  * one flag per item and player (tags gabe_<teil>): nothing is given twice; players who already have a rank
    get what they are owed once (checked every half second outside Bote scenes)
  * the items are removed from every loot table that had them (no recipe in any mod makes them)
  * Phoenix armour turned into Obsidian armour by water is turned back at once (NBT kept)
  * the Phoenix Bow gets one tagged arrow while it is held and no other arrow is there (Infinity keeps it)
  * lost an item? /trigger bote_gabe gives back what is missing (inventory, armour, ender chest, glove slot),
    cooldown CONFIG verlust.cooldown_ticks
Everything (items, ranks, enchantments, lines) is in CONFIG below. Lines/values marked ENTWURF are the user's.

Edit CONFIG, then:  py pathgen.py   and in game /reload.
"""

import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
import messengergen  # noqa: E402

PACK = messengergen.PACK
FN = "modpack:bote/pfad"

TEILE = ["waffe1", "helm", "brust", "hose", "stiefel", "handschuhe", "waffe2"]
ARMOR_SLOT = {"helm": ("armor.head", 103), "brust": ("armor.chest", 102), "hose": ("armor.legs", 101),
              "stiefel": ("armor.feet", 100)}

CONFIG = {
    # when each part is given: "wunsch" = right after the wish is chosen, otherwise the rank   (ENTWURF)
    "wann": {"waffe1": "wunsch", "helm": 3, "brust": 4, "hose": 5, "stiefel": 6, "handschuhe": 6, "waffe2": 7},
    "pfade": {
        # mes_wish value, label, colour, items: part -> (item id, [(enchantment, level), ...])      (ENTWURF)
        "macht": (1, "Macht", "red", {
            "waffe1": ("aether:pig_slayer", [("minecraft:looting", 3), ("minecraft:sharpness", 5)]),
            "helm": ("aether:obsidian_helmet", [("minecraft:protection", 4), ("minecraft:thorns", 2)]),
            "brust": ("aether:obsidian_chestplate", [("minecraft:protection", 4), ("minecraft:thorns", 2)]),
            "hose": ("aether:obsidian_leggings", [("minecraft:protection", 4), ("minecraft:thorns", 2)]),
            "stiefel": ("aether:obsidian_boots", [("minecraft:protection", 4), ("minecraft:thorns", 2)]),
            "handschuhe": ("aether:obsidian_gloves", []),
            "waffe2": ("aether:vampire_blade", [("minecraft:sharpness", 4), ("minecraft:looting", 3),
                                                ("minecraft:sweeping", 3)]),     # Schwungkraft: level not given, III = max
        }),
        "schutz": (2, "Schutz", "aqua", {
            "waffe1": ("aether:hammer_of_kingbdogz", [("minecraft:knockback", 2), ("minecraft:sharpness", 4)]),
            "helm": ("aether:valkyrie_helmet", [("minecraft:protection", 4)]),
            "brust": ("aether:valkyrie_chestplate", [("minecraft:protection", 4)]),
            "hose": ("aether:valkyrie_leggings", [("minecraft:protection", 4)]),
            "stiefel": ("aether:valkyrie_boots", [("minecraft:protection", 4), ("minecraft:feather_falling", 4)]),
            "handschuhe": ("aether:valkyrie_gloves", []),
            "waffe2": ("aether:holy_sword", [("minecraft:smite", 5), ("minecraft:looting", 3)]),
        }),
        "wissen": (3, "Wissen", "light_purple", {
            "waffe1": ("aether:phoenix_bow", [("minecraft:power", 5), ("minecraft:punch", 2), ("minecraft:infinity", 1)]),
            "helm": ("aether:phoenix_helmet", [("minecraft:fire_protection", 4), ("minecraft:protection", 3)]),
            "brust": ("aether:phoenix_chestplate", [("minecraft:fire_protection", 4), ("minecraft:protection", 3)]),
            "hose": ("aether:phoenix_leggings", [("minecraft:fire_protection", 4), ("minecraft:protection", 3)]),
            "stiefel": ("aether:phoenix_boots", [("minecraft:fire_protection", 4), ("minecraft:protection", 3)]),
            "handschuhe": ("aether:phoenix_gloves", []),
            "waffe2": ("aether:lightning_sword", [("minecraft:sharpness", 4), ("minecraft:looting", 3)]),
        }),
    },
    "lore": "Gabe des Boten",                                          # ENTWURF
    "lore_pfad": "Pfad: {pfad}",                                       # ENTWURF
    "geschenk_zeile": "Ein Geschenk. Behandelt es nicht gering.",      # ENTWURF
    "voll_warnung": "Euer Inventar ist voll - die Gabe liegt vor euren Füßen.",
    "verlust_hinweis": "Verliert ihr eine Gabe, ruft mich: ",          # ENTWURF, followed by a clickable button
    "verlust_knopf": "[Gabe zurückfordern]",
    "verlust_zeile": "Ihr seid nachlässig. Hier, nehmt es zurück.",   # ENTWURF
    "verlust_nichts": "Euch fehlt nichts.",                            # ENTWURF
    "verlust_warten": "Noch nicht. Kommt in {m} Minuten wieder.",      # ENTWURF ({m} = minutes left)
    "verlust": {"cooldown_ticks": 24000},                              # 1 in-game day (counted while online)
    # Phoenix Bow helper arrow
    "bogen": {"item": "aether:phoenix_bow", "lore": "Pfeil des Phoenix-Bogens"},
    # Phoenix -> Obsidian conversion (water): which obsidian item belongs to which phoenix item
    "phoenix_zurueck": {"helm": ("aether:obsidian_helmet", "aether:phoenix_helmet"),
                        "brust": ("aether:obsidian_chestplate", "aether:phoenix_chestplate"),
                        "hose": ("aether:obsidian_leggings", "aether:phoenix_leggings"),
                        "stiefel": ("aether:obsidian_boots", "aether:phoenix_boots"),
                        "handschuhe": ("aether:obsidian_gloves", "aether:phoenix_gloves")},
    "glove_slot": "aether_gloves",                                     # Curios slot id (checked in player data)
}

# Aether loot tables that contain path items (found by scanning every jar's data/ for the item ids)
AETHER_LOOT = ["chests/dungeon/bronze/bronze_dungeon_reward", "chests/dungeon/bronze/bronze_dungeon_treasure",
               "chests/dungeon/gold/gold_dungeon_reward", "chests/dungeon/gold/gold_dungeon_treasure",
               "chests/dungeon/silver/silver_dungeon_reward", "chests/dungeon/silver/silver_dungeon_treasure",
               "chests/dungeon/silver/silver_dungeon_valkyrie"]


def j(o):
    return json.dumps(o, ensure_ascii=False)


def lore_line(text, color):
    return "'" + j({"text": text, "color": color, "italic": False}).replace("'", "\\'") + "'"


def item_nbt(pfad, teil):
    C = CONFIG
    _, label, color, items = C["pfade"][pfad]
    iid, ench = items[teil]
    en = ",".join('{id:"%s",lvl:%ds}' % (e, lv) for e, lv in ench)
    lore = ",".join([lore_line(C["lore"], "gold"), lore_line(C["lore_pfad"].format(pfad=label), color)])
    return iid, ('{Unbreakable:1b,%sdisplay:{Lore:[%s]},modpack_questitem:1b,modpack_pfad:"%s",modpack_teil:"%s"}'
                 % (f"Enchantments:[{en}]," if en else "", lore, pfad, teil))


def check_ids():
    gd = gamedata.load()
    with zipfile.ZipFile(gamedata._client_jar()) as z:
        lang = json.loads(z.read("assets/minecraft/lang/en_us.json"))
    for pfad, (_, _, _, items) in CONFIG["pfade"].items():
        for teil, (iid, ench) in items.items():
            if iid not in gd.items:
                raise SystemExit(f"ERROR: item {iid} does not exist")
            for e, _ in ench:
                ns, name = e.split(":")
                if f"enchantment.{ns}.{name}" not in lang:
                    raise SystemExit(f"ERROR: enchantment {e} does not exist in 1.20.1")
    for a, b in CONFIG["phoenix_zurueck"].values():
        for i in (a, b):
            if i not in gd.items:
                raise SystemExit(f"ERROR: item {i} does not exist")


def has_item(iid, extra=""):
    """selector conditions: the player has this quest item in inventory/armour, ender chest or the glove slot"""
    t = '{modpack_questitem:1b%s}' % extra
    return [f'@s[nbt={{Inventory:[{{id:"{iid}",tag:{t}}}]}}]', f'@s[nbt={{EnderItems:[{{id:"{iid}",tag:{t}}}]}}]',
            f'@s[nbt={{ForgeCaps:{{"curios:inventory":{{Curios:[{{Identifier:"{CONFIG["glove_slot"]}",'
            f'StacksHandler:{{Stacks:{{Items:[{{id:"{iid}",tag:{t}}}]}}}}}}]}}}}}}]']


def build():
    C = CONFIG
    check_ids()
    voice = f"playsound {messengergen.CONFIG['voice'][0]} neutral @s ~ ~ ~ 1 {messengergen.CONFIG['voice'][1]}"
    f = {}
    f["load"] = f"""
scoreboard objectives add bote_gabe trigger
scoreboard objectives add bote_gcd dummy
scoreboard objectives add bote_pfeil dummy
schedule function {FN}/loop 10t replace
"""
    f["loop"] = f"""
# every 10 ticks
schedule function {FN}/loop 10t replace
# what each player is owed (catch-up included; nothing twice). Not during a Bote scene
execute as @a[tag=!mes_scene,scores={{mes_wish=1..3}}] at @s run function {FN}/pruefen
# Phoenix armour turned to Obsidian by water: back to Phoenix
execute as @a[scores={{mes_wish=3}}] at @s run function {FN}/phoenix/check
# Phoenix Bow helper arrow: only while the bow is held; never on the ground
execute as @a unless predicate modpack:bote/pfad/bogen_in_hand run clear @s minecraft:arrow{{modpack_bogenpfeil:1b}}
kill @e[type=minecraft:item,nbt={{Item:{{tag:{{modpack_bogenpfeil:1b}}}}}}]
# lost items: /trigger bote_gabe
scoreboard players enable @a[scores={{mes_wish=1..3}}] bote_gabe
scoreboard players remove @a[scores={{bote_gcd=1..}}] bote_gcd 10
execute as @a[scores={{bote_gabe=1..}}] at @s run function {FN}/verlust/anfrage
"""
    f["tick"] = f"""
execute as @a[predicate=modpack:bote/pfad/bogen_in_hand] run function {FN}/bogen/check
"""
    f["pruefen"] = "\n".join(
        [f"# as + at a player: gives every path item they are owed and do not have the flag for"]
        + [f"execute if score @s mes_wish matches {w} run function {FN}/pruefen/{p}"
           for p, (w, _, _, _) in C["pfade"].items()])
    for p in C["pfade"]:
        lines = [f"# as + at a {p} player"]
        for teil in TEILE:
            when = C["wann"][teil]
            cond = "" if when == "wunsch" else f"if score @s bote_rang matches {when}.. "
            lines.append(f"execute {cond}unless entity @s[tag=gabe_{teil}] run function {FN}/gib/{p}/{teil}")
        f[f"pruefen/{p}"] = "\n".join(lines)
        for teil in TEILE:
            iid, nbt = item_nbt(p, teil)
            f[f"item/{p}/{teil}"] = f"""
# the item itself (no flag, no message)
give @s {iid}{nbt} 1
"""
            f[f"gib/{p}/{teil}"] = f"""
# as + at the player: gives {iid} ({p}, {teil}) once
tag @s add gabe_{teil}
function {FN}/item/{p}/{teil}
function {FN}/gegeben
"""
            f[f"op/gib/{p}/{teil}"] = f"""
# OPERATOR: execute as <player> at @s run function {FN}/op/gib/{p}/{teil}   (gives it even if already given)
tag @s add gabe_{teil}
function {FN}/item/{p}/{teil}
"""
    btn = j(["", {"text": C["verlust_hinweis"], "color": messengergen.CONFIG["text_color"], "italic": True},
             {"text": C["verlust_knopf"], "color": "gold", "bold": True,
              "clickEvent": {"action": "run_command", "value": "/trigger bote_gabe"},
              "hoverEvent": {"action": "show_text", "contents": "/trigger bote_gabe"}}])
    f["gegeben"] = f"""
# as + at a player who just got a gift
tellraw @s {messengergen.line(C['geschenk_zeile'])}
{voice}
execute if entity @e[type=minecraft:item,distance=..3,nbt={{Age:0s,Item:{{tag:{{modpack_questitem:1b}}}}}}] run tellraw @s {j({'text': C['voll_warnung'], 'color': 'red'})}
execute unless entity @s[tag=gabe_hinweis] run tellraw @s {btn}
tag @s add gabe_hinweis
"""
    # ---------------- Phoenix -> Obsidian revert
    ph = C["phoenix_zurueck"]
    lines = ["# as + at a Wissen player: obsidian pieces of the Wissen path become Phoenix again (NBT kept)"]
    for teil, (obs, _) in ph.items():
        if teil in ARMOR_SLOT:
            slot, num = ARMOR_SLOT[teil]
            lines.append(f'execute if entity @s[nbt={{Inventory:[{{Slot:{num}b,id:"{obs}",tag:{{modpack_pfad:"wissen"}}}}]}}] '
                         f"run function {FN}/phoenix/slot_{teil}")
    gl_obs = ph["handschuhe"][0]
    lines.append(f'execute if entity @s[nbt={{ForgeCaps:{{"curios:inventory":{{Curios:[{{Identifier:"{C["glove_slot"]}",'
                 f'StacksHandler:{{Stacks:{{Items:[{{id:"{gl_obs}",tag:{{modpack_pfad:"wissen"}}}}]}}}}}}]}}}}}}] '
                 f"run function #modpack:bote/pfad_handschuh")
    lines.append("# not worn (in the inventory): replaced by a fresh Phoenix piece")
    for teil, (obs, _) in ph.items():
        lines.append(f'execute store result score #n bote_pfeil run clear @s {obs}{{modpack_pfad:"wissen"}}')
        lines.append(f"execute if score #n bote_pfeil matches 1.. run function {FN}/item/wissen/{teil}")
    f["phoenix/check"] = "\n".join(lines)
    for teil, (obs, phx) in ph.items():
        if teil in ARMOR_SLOT:
            slot, num = ARMOR_SLOT[teil]
            f[f"phoenix/slot_{teil}"] = f"""
data modify storage modpack:bote pfad.alt set from entity @s Inventory[{{Slot:{num}b}}].tag
item replace entity @s {slot} with {phx}
item modify entity @s {slot} modpack:bote/pfad/nbt_zurueck
playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.6 1.4
"""
    _, gl_nbt = item_nbt("wissen", "handschuhe")
    f["phoenix/handschuh_curios"] = f"""
# worn gloves (Curios slot): replaced with the Curios command. Linked through the function tag
# #modpack:bote/pfad_handschuh with required:false - if this command does not load, nothing else breaks
curios replace {C['glove_slot']} 0 @s with {ph['handschuhe'][1]}{gl_nbt}
"""
    # ---------------- Phoenix Bow arrow
    arrow = '{modpack_bogenpfeil:1b,display:{Lore:[%s]}}' % lore_line(C["bogen"]["lore"], "gray")
    f["bogen/check"] = f"""
# as a player holding the Phoenix Bow (every tick): exactly one helper arrow if there is no other arrow
execute store result score #a bote_pfeil run clear @s minecraft:arrow 0
execute store result score #u bote_pfeil run clear @s minecraft:arrow{{modpack_bogenpfeil:1b}} 0
execute store result score #s bote_pfeil run clear @s minecraft:spectral_arrow 0
execute store result score #t bote_pfeil run clear @s minecraft:tipped_arrow 0
scoreboard players operation #a bote_pfeil -= #u bote_pfeil
scoreboard players operation #a bote_pfeil += #s bote_pfeil
scoreboard players operation #a bote_pfeil += #t bote_pfeil
execute if score #a bote_pfeil matches 1.. if score #u bote_pfeil matches 1.. run clear @s minecraft:arrow{{modpack_bogenpfeil:1b}}
execute if score #a bote_pfeil matches 0 if score #u bote_pfeil matches 0 run give @s minecraft:arrow{arrow} 1
execute if score #a bote_pfeil matches 0 if score #u bote_pfeil matches 2.. run function {FN}/bogen/einer
"""
    f["bogen/einer"] = f"""
clear @s minecraft:arrow{{modpack_bogenpfeil:1b}}
give @s minecraft:arrow{arrow} 1
"""
    # ---------------- loss
    miss = []
    for p, (w, _, _, items) in C["pfade"].items():
        for teil in TEILE:
            iid = items[teil][0]
            conds = " ".join(f"unless entity {s}" for s in has_item(iid))
            if p == "wissen" and teil in ph:     # a converted piece still counts as "there"
                conds += " " + " ".join(f"unless entity {s}" for s in has_item(ph[teil][0], ',modpack_pfad:"wissen"'))
            miss.append(f"execute if score @s mes_wish matches {w} if entity @s[tag=gabe_{teil}] {conds} "
                        f"run function {FN}/verlust/zurueck/{p}/{teil}")
            f[f"verlust/zurueck/{p}/{teil}"] = f"""
function {FN}/item/{p}/{teil}
scoreboard players add #gab bote_pfeil 1
"""
    wa, _, wb = C["verlust_warten"].partition("{m}")
    MC = messengergen.CONFIG
    txt = {"color": MC["text_color"], "italic": True, "bold": False}
    wait_json = j(["", {"text": f"\n✦ {MC['name']} ✦ » ", "color": MC["name_color"], "bold": True},
                   {"text": wa, **txt}, {"score": {"name": "#m", "objective": "bote_pfeil"}, **txt},
                   {"text": wb, **txt}])
    f["verlust/anfrage"] = f"""
# as + at a player who ran /trigger bote_gabe
scoreboard players set @s bote_gabe 0
execute if score @s bote_gcd matches 1.. run function {FN}/verlust/warten
execute unless score @s bote_gcd matches 1.. run function {FN}/verlust/nachgeben
"""
    f["verlust/warten"] = f"""
scoreboard players operation #m bote_pfeil = @s bote_gcd
scoreboard players add #m bote_pfeil 1199
scoreboard players set #1200 bote_pfeil 1200
scoreboard players operation #m bote_pfeil /= #1200 bote_pfeil
tellraw @s {wait_json}
"""
    f["verlust/nachgeben"] = "\n".join(
        ["# as + at the player: every owed item that is nowhere on them comes back",
         "scoreboard players set #gab bote_pfeil 0"] + miss + [
            f"execute if score #gab bote_pfeil matches 1.. run tellraw @s {messengergen.line(C['verlust_zeile'])}",
            f"execute if score #gab bote_pfeil matches 1.. run {voice}",
            f"execute if score #gab bote_pfeil matches 1.. run scoreboard players set @s bote_gcd {C['verlust']['cooldown_ticks']}",
            f"execute if score #gab bote_pfeil matches 0 run tellraw @s {messengergen.line(C['verlust_nichts'])}"])
    # ---------------- operator and tests
    f["op/pruefen"] = f"""
# OPERATOR: execute as <player> at @s run function {FN}/op/pruefen
# gives what the player is owed and everything owed that is missing (ignores the cooldown)
function {FN}/pruefen
function {FN}/verlust/nachgeben
"""
    f["op/reset"] = "\n".join(
        [f"# OPERATOR: execute as <player> run function {FN}/op/reset",
         "# forgets which path items were given and removes all quest items from inventory and armour",
         *sorted({f"clear @s {i}{{modpack_questitem:1b}}" for _, _, _, its in C["pfade"].values() for i, _ in its.values()}),
         "clear @s minecraft:arrow{modpack_bogenpfeil:1b}",
         "scoreboard players set @s bote_gcd 0", "tag @s remove gabe_hinweis"]
        + [f"tag @s remove gabe_{t}" for t in TEILE])
    for p, (w, label, _, _) in C["pfade"].items():
        f[f"test/pfad_{p}"] = f"""
# TEST: your path is {label} (mes_wish {w}); the first weapon comes within half a second
scoreboard players set @s mes_wish {w}
tag @s add mes_has_wish
"""
    f["test/bogen_ohne_pfeile"] = f"""
# TEST: removes all your arrows and puts a Phoenix Bow (path item) in your hand
clear @s minecraft:arrow
clear @s minecraft:spectral_arrow
clear @s minecraft:tipped_arrow
item replace entity @s weapon.mainhand with {item_nbt('wissen', 'waffe1')[0]}{item_nbt('wissen', 'waffe1')[1]}
"""
    f["test/haltbarkeit"] = """
# TEST: shows Unbreakable and Damage of the item in your main hand (Unbreakable 1, Damage stays 0)
tellraw @s ["",{"text":"Unbreakable: "},{"nbt":"SelectedItem.tag.Unbreakable","entity":"@s"},{"text":"  Damage: "},{"nbt":"SelectedItem.tag.Damage","entity":"@s"},{"text":"  Pfad: "},{"nbt":"SelectedItem.tag.modpack_pfad","entity":"@s"}]
"""
    f["test/wasser"] = """
# TEST: a water block at your feet (Phoenix armour converts after a while, then the pack turns it back)
setblock ~ ~ ~ minecraft:water
"""
    f["test/verlust_kurz"] = """
# TEST: the cooldown of /trigger bote_gabe ends now
scoreboard players set @s bote_gcd 0
"""
    return f


def strip_entries(node, items, removed, where):
    """Removes item entries for the given ids from a loot table structure (recursively, also inside groups)."""
    if isinstance(node, dict):
        if "entries" in node:
            keep = []
            for e in node["entries"]:
                if e.get("type") == "minecraft:item" and e.get("name") in items:
                    removed.append((where, e["name"]))
                    continue
                strip_entries(e, items, removed, where)
                if "children" in e and not e["children"]:
                    continue
                keep.append(e)
            node["entries"] = keep
        if "children" in node:
            keep = []
            for e in node["children"]:
                if e.get("type") == "minecraft:item" and e.get("name") in items:
                    removed.append((where, e["name"]))
                    continue
                strip_entries(e, items, removed, where)
                keep.append(e)
            node["children"] = keep
        for k, v in node.items():
            if k not in ("entries", "children") and isinstance(v, (dict, list)):
                strip_entries(v, items, removed, where)
    elif isinstance(node, list):
        for v in node:
            strip_entries(v, items, removed, where)


def loot_overrides():
    items = {i for _, _, _, its in CONFIG["pfade"].values() for i, _ in its.values()}
    jar = next(os.path.join(gamedata.MC_DIR, "mods", n) for n in os.listdir(os.path.join(gamedata.MC_DIR, "mods"))
               if n.startswith("aether-"))
    out, removed = {}, []
    with zipfile.ZipFile(jar) as z:
        for t in AETHER_LOOT:
            d = json.loads(z.read(f"data/aether/loot_tables/{t}.json"))
            strip_entries(d, items, removed, t)
            for pool in d.get("pools", []):
                pool["entries"] = pool.get("entries", [])
            d["pools"] = [p for p in d.get("pools", []) if p["entries"]]
            out[f"data/aether/loot_tables/{t}.json"] = d
    return out, removed


def files():
    C = CONFIG
    bow = C["bogen"]["item"]
    keys = ["Enchantments", "display", "Trim", "Unbreakable", "RepairCost", "modpack_questitem", "modpack_pfad",
            "modpack_teil"]
    return {
        "data/modpack/predicates/bote/pfad/bogen_in_hand.json": {"condition": "minecraft:any_of", "terms": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"equipment": {"mainhand": {"items": [bow]}}}},
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"equipment": {"offhand": {"items": [bow]}}}}]},
        "data/modpack/item_modifiers/bote/pfad/nbt_zurueck.json": {
            "function": "minecraft:copy_nbt", "source": {"type": "minecraft:storage", "source": "modpack:bote"},
            "ops": [{"source": f"pfad.alt.{k}", "target": k, "op": "replace"} for k in keys]},
        "data/modpack/tags/functions/bote/pfad_handschuh.json": {"values": [
            {"id": f"{FN}/phoenix/handschuh_curios", "required": False}]},
    }


def main():
    fns = build()
    base = os.path.join(PACK, "data", "modpack")
    for d in ("functions/bote/pfad", "predicates/bote/pfad", "item_modifiers/bote/pfad"):
        p = os.path.join(base, *d.split("/"))
        if os.path.isdir(p):
            shutil.rmtree(p)
    out = os.path.join(base, "functions", "bote", "pfad")
    for name, body in fns.items():
        messengergen.write_function(out, name, body)
    loot, removed = loot_overrides()
    for rel, d in {**files(), **loot}.items():
        p = os.path.join(PACK, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False)
    messengergen.add_to_tag("load", f"{FN}/load")
    messengergen.add_to_tag("tick", f"{FN}/tick")
    messengergen.add_to_tag("bote/rang_aufstieg", f"{FN}/pruefen", ns="modpack")
    messengergen.add_to_tag("bote/wunsch_gewaehlt", f"{FN}/pruefen", ns="modpack")
    print(f"Wrote {len(fns)} path functions; removed from Aether loot tables:")
    for where, item in removed:
        print(f"  {where}: {item}")


if __name__ == "__main__":
    main()
