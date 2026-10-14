"""
Rangsystem beim Zeitboten  ->  config/paxi/datapacks/elytra_extras/data/modpack/functions/bote/rang/
                               config/paxi/datapacks/elytra_extras/data/modpack/advancements/bote/rang/
                               config/paxi/datapacks/elytra_extras/data/modpack/tags/...
=====================================================================================================
Every player has points (scoreboard bote_punkte) and a rank 1-7 (bote_rang, computed from the points).
Ranks show as a team prefix over the head and in the player list (teams rang_1 .. rang_7, friendly fire ON).
Each rank brings abilities (all stay active from their rank on). Everything (names, colours, thresholds,
points, abilities, German lines) is in CONFIG below; lines marked ENTWURF are the user's to edit.

Points sources (automatic, via advancements that also catch up on old progress once):
  Pakt geschlossen (deal accepted, or a wish already chosen)   CONFIG punkte.pakt
  each boss dungeon (Ashen Warlord, Tempest Herald, Hollow Magus) punkte.siegel
  each horde leader kill (repeatable)                          punkte.leader
  wish price paid / endured / survived (once)                  punkte.preis
Points from anywhere else (quest rewards, later story steps) - run as the player:
  function modpack:bote/rang/punkte_story        (+ punkte.story, e.g. a meeting point of the two paths)
  function modpack:bote/rang/punkte_klein        (+ punkte.klein, e.g. a Bote job)
  scoreboard players set #add bote_punkte <n>  then  function modpack:bote/rang/punkte_add   (any amount)
  In an FTB quest command reward:  /execute as @p run function modpack:bote/rang/punkte_story

Edit CONFIG, then:  py rankgen.py   and in game /reload.
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
import messengergen  # noqa: E402   (the Bote's chat line style and name)

PACK = messengergen.PACK
NS_DATA = os.path.join(PACK, "data", "modpack")
FN = "modpack:bote/rang"
ADV = "modpack:bote/rang"

CONFIG = {
    # rank: (title, team colour, points needed)                                    ENTWURF (names, thresholds)
    "ranks": [
        ("Sandkorn", "gray", 0),
        ("Minutenzeiger", "white", 100),
        ("Stundengänger", "yellow", 250),
        ("Tagwandler", "green", 450),
        ("Siegelträger", "aqua", 700),
        ("Zeitenwandler", "light_purple", 1000),
        ("Gefährte des Boten", "gold", 1400),
    ],
    "prefix": "[{titel}] ",                      # shown before the player's name (over the head, player list, chat)
    "punkte": {                                  # ENTWURF
        "pakt": 100,
        "siegel": 150,                           # each of the three boss dungeons
        "story": 150,                            # punkte_story: meeting points of the paths (hook)
        "leader": 15,                            # each horde leader kill
        "klein": 10,                             # punkte_klein: a Bote job (hook)
        "preis": 20,                             # wish price paid
    },
    "punkte_hinweis": "+{n} Gunst des Boten",    # action bar when points come in ({n} = amount)
    # rank-up: title on screen, sound, a line from the Bote (one rank after another, this many ticks apart)
    "aufstieg_zeile": "Ihr steigt auf, {titel}. Die Zeit vergisst nicht, wer ihr dient.",   # ENTWURF
    "aufstieg_untertitel": "Rang {n}",
    "aufstieg_sound": ("minecraft:ui.toast.challenge_complete", 1.0, 0.8),
    "aufstieg_abstand_ticks": 60,
    # Anrede (for the Bote's lines; ranks from-to)                                  ENTWURF
    "anrede": [(1, 2, "Fremder"), (3, 4, "Wanderer"), (5, 6, "Siegelträger"), (7, 7, "Gefährte")],
    # ---------------- abilities (ENTWURF values)
    "speed": {"rang": 2, "wert": 0.10},                   # +10 % walking speed (multiply_base)
    "rakete": {"rang": 3, "jede": 5},                     # every 5th used rocket comes back
    "leben": {"rang": 4, "wert": 4},                      # +4 health = +2 hearts
    "glueck": {"rang": 5, "luck": 1, "knockback": 0.2},   # +1 luck, +20 % knockback resistance
    "zeit": {                                             # rank 6 "Zeit dehnen"
        "rang": 6,
        "schleichen_ticks": 40,                           # 2 s sneaking ...
        "item": "minecraft:clock",                        # ... with this item in the main hand
        "radius": 12,
        "dauer_s": 8,
        "slowness": 3,                                    # amplifier for normal enemies (3 = Slowness IV)
        "slowness_boss": 0,                               # bosses and horde leaders (0 = Slowness I)
        "speed": 1,                                       # player: Speed II
        "cooldown_s": 180,
        "sound": ("minecraft:block.beacon.activate", 1.0, 0.6),
        "bereit": "⌛ Zeit dehnen bereit (2 s schleichen)",            # action bar while holding the clock
        "warten": "⌛ Zeit dehnen: noch {s} s",
    },
    "atem": {                                             # rank 7 "Letzter Atemzug"
        "rang": 7,
        "schwelle": 4,                                    # health (half hearts) at or below which it fires
        "absorption": 1, "absorption_s": 10,              # Absorption II for 10 s
        "resistenz": 2, "resistenz_s": 5,                 # Resistance III for 5 s
        "cooldown_s": 600,
        "sound": ("minecraft:item.totem.use", 0.6, 1.2),
        "text": "Letzter Atemzug",
    },
    # enemies slowed by Zeit dehnen (checked against the installed game; bosses get slowness_boss)
    "feinde": ["minecraft:zombie", "minecraft:husk", "minecraft:drowned", "minecraft:zombie_villager",
               "minecraft:skeleton", "minecraft:stray", "minecraft:wither_skeleton", "minecraft:spider",
               "minecraft:cave_spider", "minecraft:creeper", "minecraft:witch", "minecraft:slime",
               "minecraft:magma_cube", "minecraft:blaze", "minecraft:ghast", "minecraft:phantom",
               "minecraft:pillager", "minecraft:vindicator", "minecraft:evoker", "minecraft:illusioner",
               "minecraft:ravager", "minecraft:vex", "minecraft:guardian", "minecraft:shulker",
               "minecraft:silverfish", "minecraft:endermite", "minecraft:piglin_brute", "minecraft:hoglin",
               "minecraft:zoglin",
               "aether:zephyr", "aether:cockatrice", "aether:sentry", "aether:mimic", "aether:aechor_plant",
               "aether:fire_minion", "aether:valkyrie", "aether:evil_whirlwind"],
    "feinde_boss": ["minecraft:wither", "minecraft:warden", "minecraft:elder_guardian", "minecraft:ender_dragon",
                    "aether:slider", "aether:valkyrie_queen", "aether:sun_spirit"],
    "boss_tags": ["ed_boss", "modpack_horde_leader"],     # entity tags of our bosses and horde leaders
    # sources (existing advancements)
    "siegel": {"ashen": "elytra_dungeons:bosses/ashen_warlord", "storm": "elytra_dungeons:bosses/tempest_herald",
               "hollow": "elytra_dungeons:bosses/hollow_magus"},
    "pakt_aus": ["elytra_extras:bote/pakt", "elytra_extras:bote/wish_macht", "elytra_extras:bote/wish_schutz",
                 "elytra_extras:bote/wish_wissen"],
    "preis_aus": ["elytra_extras:bote/macht_paid", "elytra_extras:bote/schutz_endured",
                  "elytra_extras:bote/wissen_survived"],
    "leader_tag": "modpack_horde_leader",
}

# fixed modifier UUIDs (never change them, or old modifiers stay on players)
UUID = {"speed": "6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e1", "leben": "6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e2",
        "luck": "6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e3", "knockback": "6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e4"}


def j(obj):
    return json.dumps(obj, ensure_ascii=False)


def build():
    C = CONFIG
    gd = gamedata.load()
    for s in (C["aufstieg_sound"][0], C["zeit"]["sound"][0], C["atem"]["sound"][0]):
        if s not in gd.sounds:
            raise SystemExit(f"ERROR: sound {s} does not exist")
    for e in C["feinde"] + C["feinde_boss"]:
        if e not in gd.entities:
            raise SystemExit(f"ERROR: entity {e} does not exist")
    if C["zeit"]["item"] not in gd.items:
        raise SystemExit(f"ERROR: item {C['zeit']['item']} does not exist")
    for st in ("minecraft:sneak_time", "minecraft:leave_game"):
        if st not in gd.stats:
            raise SystemExit(f"ERROR: stat {st} does not exist")
    R, P, Z, A = C["ranks"], C["punkte"], C["zeit"], C["atem"]
    n_ranks = len(R)
    f = {}
    teams = "\n".join(
        f"team add rang_{i}\n"
        f"team modify rang_{i} prefix {j({'text': C['prefix'].format(titel=t), 'color': col})}\n"
        f"team modify rang_{i} color {col}\n"
        f"team modify rang_{i} friendlyFire true\n"
        f"team modify rang_{i} nametagVisibility always" for i, (t, col, _) in enumerate(R, 1))
    f["load"] = f"""
# Rangsystem: scoreboards, teams, loop
scoreboard objectives add bote_punkte dummy
scoreboard objectives add bote_rang dummy
scoreboard objectives add bote_ziel dummy
scoreboard objectives add bote_rwait dummy
scoreboard objectives add bote_rkt minecraft.used:minecraft.firework_rocket
scoreboard objectives add bote_rkn dummy
scoreboard objectives add bote_snk minecraft.custom:minecraft.sneak_time
scoreboard objectives add bote_snc dummy
scoreboard objectives add bote_cd6 dummy
scoreboard objectives add bote_cd7 dummy
scoreboard objectives add bote_hp health
scoreboard objectives add bote_anr dummy
scoreboard players set #20 bote_rang 20
{teams}
# the old manual friendly-fire team: players now sit in the rank teams (friendly fire on there)
team remove friends
schedule function {FN}/loop 10t replace
"""
    ziel = "\n".join(f"execute if score @s bote_punkte matches {pts}.. run scoreboard players set @s bote_ziel {i}"
                     for i, (_, _, pts) in enumerate(R, 1))
    team_heal = "\n".join(f"execute as @a[scores={{bote_rang={i}}},team=!rang_{i}] run team join rang_{i} @s"
                          for i in range(1, n_ranks + 1))
    f["loop"] = f"""
# every 10 ticks
schedule function {FN}/loop 10t replace
# new players: rank 1, 0 points
execute as @a unless score @s bote_punkte matches -2147483648.. run scoreboard players set @s bote_punkte 0
execute as @a unless score @s bote_rang matches 1.. run scoreboard players set @s bote_rang 1
scoreboard players add @a bote_cd6 0
scoreboard players add @a bote_cd7 0
# rank from points; going up one rank at a time with the ceremony (not during a Bote scene), down at once
execute as @a run function {FN}/ziel
scoreboard players remove @a[scores={{bote_rwait=1..}}] bote_rwait 10
execute as @a[tag=!mes_scene] if score @s bote_rang < @s bote_ziel unless score @s bote_rwait matches 1.. at @s run function {FN}/aufstieg
execute as @a if score @s bote_rang > @s bote_ziel run function {FN}/abstieg
{team_heal}
# abilities (passive ones are checked every time: login, respawn, rank change all covered)
execute as @e[type=minecraft:player] run function {FN}/faehigkeiten
execute as @e[type=minecraft:player,tag=!mes_scene,scores={{bote_rang={C['rakete']['rang']}..,bote_rkt=1..}}] at @s run function {FN}/rakete
scoreboard players set @a bote_rkt 0
scoreboard players remove @a[scores={{bote_cd6=1..}}] bote_cd6 10
scoreboard players remove @a[scores={{bote_cd7=1..}}] bote_cd7 10
execute as @a[scores={{bote_rang={Z['rang']}..}},predicate=modpack:bote/rang/uhr_in_hand] run function {FN}/zeit/anzeige
"""
    f["tick"] = f"""
# every tick, only for players with the active abilities
execute as @e[type=minecraft:player,scores={{bote_rang={Z['rang']}..}}] at @s run function {FN}/zeit/check
execute as @e[type=minecraft:player,tag=!mes_scene,scores={{bote_rang={A['rang']}..,bote_cd7=..0,bote_hp=1..{A['schwelle']}}}] at @s run function {FN}/atem/ausloesen
"""
    f["ziel"] = f"""
# as a player: bote_ziel = the rank their points are worth
scoreboard players set @s bote_ziel 1
{ziel}
"""
    f["aufstieg"] = f"""
# as + at a player: one rank up, with title, sound and a line from the Bote
scoreboard players add @s bote_rang 1
scoreboard players set @s bote_rwait {C['aufstieg_abstand_ticks']}
""" + "\n".join(f"execute if score @s bote_rang matches {i} run function {FN}/aufstieg/{i}"
                for i in range(2, n_ranks + 1)) + f"""
function {FN}/faehigkeiten
# HOOK: everything that comes with a new rank (path rewards, shop, jobs) listens to this function tag
function #modpack:bote/rang_aufstieg
"""
    snd = C["aufstieg_sound"]
    for i, (t, col, _) in enumerate(R, 1):
        if i == 1:
            continue
        f[f"aufstieg/{i}"] = f"""
# rank {i}: {t}
team join rang_{i} @s
title @s times 10 70 20
title @s subtitle {j({'text': C['aufstieg_untertitel'].format(n=i), 'color': 'gray'})}
title @s title {j({'text': t, 'color': col, 'bold': True})}
playsound {snd[0]} player @s ~ ~ ~ {snd[1]} {snd[2]}
tellraw @s {messengergen.line(C['aufstieg_zeile'].format(titel=t))}
"""
    f["abstieg"] = f"""
# as a player whose points are worth less than their rank (only by operator): set at once, no ceremony
scoreboard players operation @s bote_rang = @s bote_ziel
scoreboard players set @s bote_rwait 0
function {FN}/faehigkeiten
"""
    sp, lb, gl = C["speed"], C["leben"], C["glueck"]
    f["faehigkeiten"] = f"""
# as a player: passive abilities on or off for their rank. Fixed UUIDs: adding an existing one fails, so
# nothing stacks; health is never lowered by re-adding
execute if score @s bote_rang matches {sp['rang']}.. run attribute @s minecraft:generic.movement_speed modifier add {UUID['speed']} bote_rang_speed {sp['wert']} multiply_base
execute unless score @s bote_rang matches {sp['rang']}.. run attribute @s minecraft:generic.movement_speed modifier remove {UUID['speed']}
execute if score @s bote_rang matches {lb['rang']}.. run attribute @s minecraft:generic.max_health modifier add {UUID['leben']} bote_rang_leben {lb['wert']} add
execute unless score @s bote_rang matches {lb['rang']}.. run attribute @s minecraft:generic.max_health modifier remove {UUID['leben']}
execute if score @s bote_rang matches {gl['rang']}.. run attribute @s minecraft:generic.luck modifier add {UUID['luck']} bote_rang_luck {gl['luck']} add
execute unless score @s bote_rang matches {gl['rang']}.. run attribute @s minecraft:generic.luck modifier remove {UUID['luck']}
execute if score @s bote_rang matches {gl['rang']}.. run attribute @s minecraft:generic.knockback_resistance modifier add {UUID['knockback']} bote_rang_knockback {gl['knockback']} add
execute unless score @s bote_rang matches {gl['rang']}.. run attribute @s minecraft:generic.knockback_resistance modifier remove {UUID['knockback']}
"""
    rk = C["rakete"]
    f["rakete"] = f"""
# as + at a player (rank {rk['rang']}+, not in a Bote scene) who used rockets: every {rk['jede']}th comes back
scoreboard players operation @s bote_rkn += @s bote_rkt
scoreboard players set @s bote_rkt 0
function {FN}/rakete_zurueck
"""
    f["rakete_zurueck"] = f"""
execute if score @s bote_rkn matches {rk['jede']}.. run give @s minecraft:firework_rocket 1
execute if score @s bote_rkn matches {rk['jede']}.. run scoreboard players remove @s bote_rkn {rk['jede']}
execute if score @s bote_rkn matches {rk['jede']}.. run function {FN}/rakete_zurueck
"""
    # ---------------- Zeit dehnen
    feinde = f"@e[type=#modpack:bote/feindlich,distance=..{Z['radius']}," + ",".join(f"tag=!{t}" for t in C["boss_tags"]) + "]"
    f["zeit/check"] = f"""
# as + at a player with rank {Z['rang']}+ (every tick): counts sneaking ticks while holding the {Z['item']}
execute if score @s bote_snk matches 1.. if predicate modpack:bote/rang/uhr_in_hand run scoreboard players add @s bote_snc 1
execute unless score @s bote_snk matches 1.. run scoreboard players set @s bote_snc 0
execute unless predicate modpack:bote/rang/uhr_in_hand run scoreboard players set @s bote_snc 0
scoreboard players set @s bote_snk 0
execute if score @s bote_snc matches {Z['schleichen_ticks']}.. if entity @s[tag=!mes_scene] unless score @s bote_cd6 matches 1.. run function {FN}/zeit/ausloesen
execute if score @s bote_snc matches {Z['schleichen_ticks']}.. run scoreboard players set @s bote_snc 0
"""
    zs = Z["sound"]
    f["zeit/ausloesen"] = f"""
# as + at the player: enemies around are slowed, the player gets faster, cooldown starts
effect give {feinde} minecraft:slowness {Z['dauer_s']} {Z['slowness']} false
effect give @e[type=#modpack:bote/feindlich_boss,distance=..{Z['radius']}] minecraft:slowness {Z['dauer_s']} {Z['slowness_boss']} false
""" + "\n".join(f"effect give @e[tag={t},distance=..{Z['radius']}] minecraft:slowness {Z['dauer_s']} {Z['slowness_boss']} false"
                for t in C["boss_tags"]) + f"""
effect give @s minecraft:speed {Z['dauer_s']} {Z['speed']} true
playsound {zs[0]} player @a[distance=..16] ~ ~ ~ {zs[1]} {zs[2]}
particle minecraft:reverse_portal ~ ~1 ~ 4 1 4 0.02 200
scoreboard players set @s bote_cd6 {Z['cooldown_s'] * 20}
"""
    warten_a, _, warten_b = Z["warten"].partition("{s}")
    f["zeit/anzeige"] = f"""
# as a player holding the clock: cooldown or "ready" in the action bar
execute unless score @s bote_cd6 matches 1.. run title @s actionbar {j({'text': Z['bereit'], 'color': 'gray'})}
execute if score @s bote_cd6 matches 1.. store result score #s bote_rang run scoreboard players get @s bote_cd6
execute if score @s bote_cd6 matches 1.. run scoreboard players operation #s bote_rang /= #20 bote_rang
execute if score @s bote_cd6 matches 1.. run title @s actionbar {j(['', {'text': warten_a, 'color': 'dark_gray'}, {'score': {'name': '#s', 'objective': 'bote_rang'}, 'color': 'dark_gray'}, {'text': warten_b, 'color': 'dark_gray'}])}
"""
    asnd = A["sound"]
    f["atem/ausloesen"] = f"""
# as + at a player with very little health (rank {A['rang']}+, not in a Bote scene): a short shield, then cooldown
effect give @s minecraft:absorption {A['absorption_s']} {A['absorption']} false
effect give @s minecraft:resistance {A['resistenz_s']} {A['resistenz']} false
playsound {asnd[0]} player @a[distance=..16] ~ ~ ~ {asnd[1]} {asnd[2]}
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.3 40
title @s actionbar {j({'text': A['text'], 'color': 'gold'})}
scoreboard players set @s bote_cd7 {A['cooldown_s'] * 20}
"""
    # ---------------- points
    hint_a, _, hint_b = C["punkte_hinweis"].partition("{n}")
    f["punkte_add"] = f"""
# as a player: + #add bote_punkte points (set #add first: scoreboard players set #add bote_punkte <n>)
scoreboard players operation @s bote_punkte += #add bote_punkte
title @s actionbar {j(['', {'text': hint_a, 'color': 'gold'}, {'score': {'name': '#add', 'objective': 'bote_punkte'}, 'color': 'gold'}, {'text': hint_b, 'color': 'gold'}])}
"""
    for name, key, what in (("punkte_story", "story", "a story step (e.g. the paths meet)"),
                            ("punkte_klein", "klein", "a small deed (e.g. a Bote job)"),
                            ("quelle/pakt", "pakt", "the pact with the Bote"),
                            ("quelle/siegel", "siegel", "a seal (boss dungeon)"),
                            ("quelle/treffpunkt", "story", "HOOK: a meeting point of the paths"),
                            ("quelle/leader", "leader", "a horde leader kill"),
                            ("quelle/auftrag", "klein", "HOOK: a Bote job done"),
                            ("quelle/preis", "preis", "a wish price paid")):
        f[name] = f"""
# as a player: +{P[key]} points for {what}
scoreboard players set #add bote_punkte {P[key]}
function {FN}/punkte_add
"""
    f["quelle/leader_kill"] = f"""
# advancement reward (repeatable): a horde leader was killed by this player
advancement revoke @s only {ADV}/leader_kill
function {FN}/quelle/leader
"""
    # ---------------- Anrede and hooks
    anr = "\n".join(
        f"execute if score @s bote_rang matches {a}..{b} run data modify storage modpack:bote anrede set value {j(text)}\n"
        f"execute if score @s bote_rang matches {a}..{b} run scoreboard players set @s bote_anr {k}"
        for k, (a, b, text) in enumerate(C["anrede"], 1))
    f["anrede"] = f"""
# as a player: puts the Bote's form of address for this player's rank into storage modpack:bote anrede
# (and bote_anr = 1..{len(C['anrede'])}). Use it in a line right after calling this function:
#   function modpack:bote/rang/anrede
#   tellraw @s ["",{{"text":"Seid gegrüßt, "}},{{"storage":"modpack:bote","nbt":"anrede"}},{{"text":"."}}]
{anr}
"""
    f["hook/sortiment"] = """
# HOOK (placeholder, not called yet): as + at a Bote, mes_cur = his player.
# Later: add trades by rank, e.g.
#   execute if entity @a[tag=mes_cur,scores={bote_rang=3..}] run data modify entity @s Offers.Recipes append value {...}
"""
    f["hook/auftraege"] = """
# HOOK (placeholder, not called yet): as a player. Later: offer Bote jobs from a certain rank on, e.g.
#   execute if score @s bote_rang matches 4.. run function ...
# and reward a finished job with:  function modpack:bote/rang/quelle/auftrag
"""
    # ---------------- operator commands
    f["op/punkte_setzen"] = f"""
# OPERATOR: scoreboard players set #wert bote_punkte <n>  then  execute as <player> run function {FN}/op/punkte_setzen
# (or simply: /scoreboard players set <player> bote_punkte <n>; the rank follows within half a second)
scoreboard players operation @s bote_punkte = #wert bote_punkte
"""
    for i, (t, _, pts) in enumerate(R, 1):
        f[f"op/rang_{i}"] = f"""
# OPERATOR: execute as <player> run function {FN}/op/rang_{i}   -> rank {i} ({t}): points set to {pts}
scoreboard players set @s bote_punkte {pts}
"""
    f["op/reset"] = f"""
# OPERATOR: execute as <player> run function {FN}/op/reset   -> rank 1, 0 points, abilities off, cooldowns cleared
# (story points already earned are not given again; use op/nachtrag for that)
scoreboard players set @s bote_punkte 0
scoreboard players set @s bote_ziel 1
scoreboard players set @s bote_rang 1
scoreboard players set @s bote_rwait 0
scoreboard players set @s bote_cd6 0
scoreboard players set @s bote_cd7 0
scoreboard players set @s bote_rkn 0
team join rang_1 @s
function {FN}/faehigkeiten
"""
    f["op/nachtrag"] = f"""
# OPERATOR: execute as <player> run function {FN}/op/nachtrag
# forgets which story points were paid out; they come again (once) for everything the player has done
advancement revoke @s from {ADV}/root
"""
    f["op/neu_anwenden"] = f"""
# OPERATOR: execute as <player> run function {FN}/op/neu_anwenden   -> team and abilities for the current rank
""" + "\n".join(f"execute if score @s bote_rang matches {i} run team join rang_{i} @s" for i in range(1, n_ranks + 1)) + f"""
function {FN}/faehigkeiten
"""
    names = "\n".join(f"execute if score @s bote_rang matches {i} run data modify storage modpack:bote titel set value {j(t)}"
                      for i, (t, _, _) in enumerate(R, 1))
    state = j(["", {"text": "[Rang] ", "color": "gold"}, {"selector": "@s"}, ": ",
               {"storage": "modpack:bote", "nbt": "titel"}, " (", {"score": {"name": "@s", "objective": "bote_rang"}},
               ") | Punkte ", {"score": {"name": "@s", "objective": "bote_punkte"}},
               " | Ziel ", {"score": {"name": "@s", "objective": "bote_ziel"}},
               " | Zeit dehnen CD ", {"score": {"name": "@s", "objective": "bote_cd6"}},
               " | Atemzug CD ", {"score": {"name": "@s", "objective": "bote_cd7"}},
               " | Raketen ", {"score": {"name": "@s", "objective": "bote_rkn"}}, "/", str(rk["jede"])])
    f["op/zustand"] = f"""
# OPERATOR: function {FN}/op/zustand  (your own state)  or  execute as <player> run function {FN}/op/zustand
# The text goes to that player and to everyone tagged bote_admin (once: /tag @s add bote_admin). Cooldowns in ticks.
{names}
tellraw @s[tag=!bote_admin] {state}
tellraw @a[tag=bote_admin] {state}
"""
    # ---------------- tests
    f["test/zeit_dehnen"] = f"""
# TEST: Zeit dehnen right now (ignores rank, clock and cooldown)
function {FN}/zeit/ausloesen
"""
    f["test/atemzug"] = f"""
# TEST: Letzter Atemzug right now (ignores rank, health and cooldown)
function {FN}/atem/ausloesen
"""
    f["test/atemzug_echt"] = f"""
# TEST: the real trigger: you drop to {A['schwelle'] // 2 + 1} hearts or less (needs rank {A['rang']}, no cooldown)
effect clear @s minecraft:resistance
damage @s 15 minecraft:magic
"""
    f["test/cooldowns_kurz"] = f"""
# TEST: both cooldowns end in 5 seconds
execute if score @s bote_cd6 matches 101.. run scoreboard players set @s bote_cd6 100
execute if score @s bote_cd7 matches 101.. run scoreboard players set @s bote_cd7 100
"""
    f["test/rakete"] = f"""
# TEST: the next used rocket is the {rk['jede']}th (needs rank {rk['rang']})
scoreboard players set @s bote_rkn {rk['jede'] - 1}
"""
    return f


def files():
    """Advancements (triggers for points; they also pay out once for progress made before) and tags."""
    C = CONFIG
    out = {}
    out["advancements/bote/rang/root.json"] = {"criteria": {"done": {"trigger": "minecraft:impossible"}}}

    def has_any(advs):
        return {f"a{i}": {"trigger": "minecraft:tick", "conditions": {"player": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"player": {"advancements": {a: True}}}}]}} for i, a in enumerate(advs)}

    def adv(advs, reward):
        crit = has_any(advs)
        return {"parent": f"{ADV}/root", "criteria": crit, "requirements": [list(crit)],
                "rewards": {"function": f"{FN}/{reward}"}}

    out["advancements/bote/rang/pakt.json"] = adv(C["pakt_aus"], "quelle/pakt")
    for k, a in C["siegel"].items():
        out[f"advancements/bote/rang/siegel_{k}.json"] = adv([a], "quelle/siegel")
    out["advancements/bote/rang/preis.json"] = adv(C["preis_aus"], "quelle/preis")
    out["advancements/bote/rang/leader_kill.json"] = {
        "parent": f"{ADV}/root",
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"nbt": "{Tags:[\"%s\"]}" % C["leader_tag"]}}]}}},
        "rewards": {"function": f"{FN}/quelle/leader_kill"}}
    out["predicates/bote/rang/uhr_in_hand.json"] = {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"equipment": {"mainhand": {"items": [C["zeit"]["item"]]}}}}
    out["tags/entity_types/bote/feindlich.json"] = {"values": C["feinde"]}
    out["tags/entity_types/bote/feindlich_boss.json"] = {"values": C["feinde_boss"]}
    return out


def main():
    fns = build()
    out = os.path.join(NS_DATA, "functions", "bote", "rang")
    for d in (out, os.path.join(NS_DATA, "advancements", "bote", "rang"), os.path.join(NS_DATA, "predicates", "bote", "rang"),
              os.path.join(NS_DATA, "tags", "entity_types", "bote")):
        if os.path.isdir(d):
            shutil.rmtree(d)
    for name, body in fns.items():
        messengergen.write_function(out, name, body)
    for rel, d in files().items():
        p = os.path.join(NS_DATA, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False)
    messengergen.add_to_tag("load", f"{FN}/load")
    messengergen.add_to_tag("tick", f"{FN}/tick")
    messengergen.add_to_tag("bote/rang_aufstieg", ns="modpack")     # hook tag (pathgen adds to it)
    print(f"Wrote {len(fns)} rank functions to elytra_extras (modpack:bote/rang)")


if __name__ == "__main__":
    main()
