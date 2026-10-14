"""
Horde leaders (mini-bosses)  ->  added to the elytra_hordes Paxi datapack
=========================================================================
Every roaming horde (modpack:horde/*) gets ONE leader of a special type. All numbers are in CONFIG below:
edit, then run

    py leadergen.py           write the leader files into config/paxi/datapacks/elytra_hordes (backup first)
    py leadergen.py --check   build in memory only

Why a generator: in 1.20.1 commands like damage, effect, summon and selector distances only take literal
numbers (no macros, no /random), so the only way to keep every value in one place is to write the
functions from this table. In game, /reload applies the result.

Files owned by this script (rewritten every run, everything else in the pack is left alone):
  data/modpack/functions/leader/   data/modpack/loot_tables/leaders/
  data/modpack/advancements/leaders/   data/modpack/predicates/leader/   README_leaders.md
Hooks it adds once to the horde pack: load.json / tick.json entries, one line in horde/spawn_horde
(spawn the leader) and one in horde/clear (remove leaders too).
"""

import datetime
import json
import os
import shutil
import sys
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
from structlib import BuildError, ammo_entry, att_entry, check_items, item_entry, pool  # noqa: E402

PACK = os.path.join(gamedata.MC_DIR, "config", "paxi", "datapacks", "elytra_hordes")

# =============================================================================== CONFIG
CONFIG = {
    # selection: weights (any positive numbers); the same type never comes twice in a row
    "weights": {"laeufer": 30, "spucker": 20, "kriecher": 15, "platzer": 15, "brecher": 10, "schreier": 10},
    "max_leaders_near": 2,        # no new leader if this many are loaded within leader_cap_radius of the horde
    "leader_cap_radius": 160,
    "bossbar_range": 48,          # players within this range see the leader's bossbar
    "cue_range": 40,              # type sound plays when a player is this close ...
    "cue_cooldown_s": 8,          # ... at most every this many seconds
    "despawn_player_range": 64,   # a leader with no player this close ...
    "despawn_after_s": 180,       # ... for this long is removed (no drops)
    "break_radius": 48,           # on leader death: horde zombies this close lose their target ...
    "break_seconds": 6,           # ... for this long (follow range 0 + Slowness II), then normal again
    "follow_range_normal": 48,    # follow range horde zombies return to (the horde pack uses 48)

    "types": {
        "laeufer": {"name": "Läufer", "entity": "minecraft:zombie", "hp": 24, "speed": 0.25, "damage": 4,
                    "sprint_range": 24, "sprint_amplifier": 2},          # Speed III while it has a target within range
        "brecher": {"name": "Brecher", "entity": "minecraft:zombie", "hp": 100, "speed": 0.17, "damage": 7,
                    "armor": 30, "toughness": 20, "knockback_res": 1.0, "scale": 1.25},  # armor 30 / toughness 20 = vanilla maximum
        "spucker": {"name": "Spucker", "entity": "minecraft:husk", "hp": 40, "speed": 0.18, "damage": 3,
                    "spit_every_s": 3, "spit_min": 8, "spit_max": 24, "spit_speed": 1.4, "spit_lift": 0.35,
                    "poison_s": 5, "poison_amplifier": 0, "retreat_below": 8, "retreat_step": 0.45},
        "schreier": {"name": "Schreier", "entity": "minecraft:zombie_villager", "hp": 50, "speed": 0.21, "damage": 3,
                     "scream_every_s": 15, "scream_range": 32, "zombies_per_scream": 2, "zombie_cap": 6,
                     "gunfire_speedup_s": 1},  # every 0.25 s of nearby UNsuppressed gunfire adds this to the timer
        "kriecher": {"name": "Kriecher", "entity": "minecraft:zombie", "hp": 30, "speed": 0.27, "damage": 3,
                     "height": 0.45, "width": 1.2, "light_min": 8, "grab_slow_s": 3, "grab_slow_amplifier": 2},
        "platzer": {"name": "Platzer", "entity": "minecraft:drowned", "hp": 40, "speed": 0.2, "damage": 3,
                    "width": 1.5, "height": 1.1, "blast_inner": 2.5, "blast_outer": 5,
                    "damage_inner": 14, "damage_outer": 6, "grief_blocks": False},
    },
    # loot (dropped by the leader itself via DeathLootTable). rare = extra pool with rare_chance.
    "rare_chance": 0.1,
}

# fixed per-type look and sound (not balance values)
STYLE = {
    "laeufer": {"n": 1, "team": "yellow", "bar": "yellow", "dust": "1.0 0.9 0.2", "cue": ("minecraft:entity.husk.ambient", 1.7)},
    "brecher": {"n": 2, "team": "red", "bar": "red", "dust": "0.8 0.1 0.1", "cue": ("minecraft:entity.ravager.step", 0.8)},
    "spucker": {"n": 3, "team": "green", "bar": "green", "dust": "0.4 1.0 0.2", "cue": ("minecraft:entity.llama.spit", 0.7)},
    "schreier": {"n": 4, "team": "light_purple", "bar": "purple", "dust": "0.9 0.4 1.0", "cue": ("minecraft:entity.zombie_villager.ambient", 1.6)},
    "kriecher": {"n": 5, "team": "aqua", "bar": "blue", "dust": "0.3 0.9 1.0", "cue": ("minecraft:entity.spider.ambient", 0.6)},
    "platzer": {"n": 6, "team": "gold", "bar": "pink", "dust": "1.0 0.6 0.1", "cue": ("minecraft:entity.creeper.primed", 0.6)},
}
SILENCERS = ["knight_qd", "mirage", "phantom_s1", "ptilopsis", "sg", "ursus", "vulture", "wraith"]


def loot_tables():
    r = CONFIG["rare_chance"]
    return {
        "laeufer": [pool([ammo_entry("12g", (18, 36))]), pool([att_entry("muzzle_choke_sg")], chance=0.3),
                    pool([att_entry("shotgun_extended_mag_1")], chance=r)],
        "brecher": [pool([ammo_entry("338", (10, 20), 1), ammo_entry("50bmg", (8, 15), 1)]),
                    pool([att_entry("ammo_mod_fmj")], chance=0.3), pool([att_entry("ammo_mod_slug")], chance=r)],
        "spucker": [pool([ammo_entry("30_06", (18, 30), 1), ammo_entry("792x57", (18, 30), 1)]),
                    pool([att_entry("scope_vudu")], chance=0.2), pool([att_entry("scope_standard_8x")], chance=r)],
        "schreier": [pool([att_entry("muzzle_silencer_mirage", 2), att_entry("muzzle_silencer_ptilopsis", 1)], chance=0.6),
                     pool([ammo_entry("9mm", (20, 40))]), pool([att_entry("muzzle_silencer_vulture")], chance=r)],
        "kriecher": [pool([item_entry("torch", (8, 16))]), pool([item_entry("glowstone_dust", (4, 8))]),
                     pool([att_entry("laser_compact")], chance=0.25), pool([att_entry("laser_peq6")], chance=r)],
        "platzer": [pool([item_entry("gunpowder", (4, 10))]), pool([item_entry("tnt", (1, 2))], chance=0.3),
                    pool([ammo_entry("40mm", (2, 4))], chance=r)],
    }


# =============================================================================== builder

def T(text, **kw):
    return Template(text.strip("\n")).substitute(**kw) + "\n"


def num(x):
    return f"{x:g}"


def build():
    C, Ty = CONFIG, CONFIG["types"]
    files = {}

    def fn(path, text, **kw):
        files[f"data/modpack/functions/leader/{path}.mcfunction"] = T(text, **kw)

    def js(path, data):
        files[path] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    order = list(C["weights"])
    if set(order) != set(Ty) or set(order) != set(STYLE):
        raise BuildError("weights, types and STYLE must list the same six leader types")
    total = sum(C["weights"].values())
    tick = lambda s: int(round(s * 20))  # noqa: E731

    # ---------------- load / loop / tick
    teams = "\n".join(f"team add ld_{t}\nteam modify ld_{t} color {STYLE[t]['team']}\n"
                      f"team modify ld_{t} nametagVisibility never" for t in order)
    bars = "\n".join(
        f'bossbar add modpack:leader_{t} {{"text":"{Ty[t]["name"]}"}}\n'
        f'bossbar set modpack:leader_{t} name {{"text":"{Ty[t]["name"]}","color":"{STYLE[t]["team"]}","bold":true}}\n'
        f"bossbar set modpack:leader_{t} color {STYLE[t]['bar']}\nbossbar set modpack:leader_{t} style notched_6\n"
        f"bossbar set modpack:leader_{t} visible false" for t in order)
    objs = "\n".join(f"scoreboard objectives add {o} dummy" for o in
                     ("ld_id", "ld_type", "ld_hp", "ld_t", "ld_age", "ld_sum", "ld_cue", "ld_tmp", "ld_last", "ld_brk"))
    fn("load", """
# Runs on load (#minecraft:load). Leader teams hide nametags, which also makes Neat skip their health bar.
$objs
scoreboard players set #6 ld_tmp 6
scoreboard players add #next ld_id 0
scoreboard players add #last ld_last 0
scoreboard players set #force ld_tmp 0
$teams
$bars
schedule function modpack:leader/loop 5t replace
""", objs=objs, teams=teams, bars=bars)
    fn("loop", """
# Every 5 ticks; only loaded leaders, link markers and briefly "broken" horde zombies are touched.
schedule function modpack:leader/loop 5t replace
execute as @e[type=minecraft:marker,tag=ld_link] at @s run function modpack:leader/link_check
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/leader_tick
execute as @e[tag=ld_broken] run function modpack:leader/broken_tick
""")
    fn("tick", """
# Every tick: each leader's link marker follows it (the marker remembers where the leader died).
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/follow
""")
    fn("follow", """
scoreboard players operation #id ld_tmp = @s ld_id
execute as @e[type=minecraft:marker,tag=ld_link,distance=..64] if score @s ld_id = #id ld_tmp run tp @s ~ ~ ~
""")

    # ---------------- spawning and selection
    fn("spawn", """
# Called by horde/spawn_horde, as + at the horde's spot marker after the horde spawned.
scoreboard players set #ok ld_tmp 1
execute store result score #n ld_tmp if entity @e[tag=modpack_horde_leader,distance=..$cr]
execute if score #n ld_tmp matches $cap.. run scoreboard players set #ok ld_tmp 0
execute if score #force ld_tmp matches 1.. run scoreboard players set #ok ld_tmp 1
execute if score #ok ld_tmp matches 1 run function modpack:leader/pick
scoreboard players set #force ld_tmp 0
""", cr=C["leader_cap_radius"], cap=C["max_leaders_near"])
    fn("pick", """
execute if score #force ld_tmp matches 1.. run scoreboard players operation #type ld_tmp = #force ld_tmp
scoreboard players set #tries ld_tmp 0
execute unless score #force ld_tmp matches 1.. run function modpack:leader/roll
scoreboard players operation #last ld_last = #type ld_tmp
function modpack:leader/spawn_type
""")
    ranges, lo = [], 0
    for t in order:
        w = C["weights"][t]
        ranges.append(f"execute if score #p ld_tmp matches {lo}..{lo + w - 1} run scoreboard players set #type ld_tmp {STYLE[t]['n']}")
        lo += w
    fn("roll", """
# Weighted pick (total weight $total); re-rolls up to 8 times if it equals the last type, then takes the next type.
function modpack:horde/random
scoreboard players operation #p ld_tmp = #r mh_tmp
scoreboard players set #w ld_tmp $total
scoreboard players operation #p ld_tmp %= #w ld_tmp
$ranges
scoreboard players add #tries ld_tmp 1
execute if score #type ld_tmp = #last ld_last if score #tries ld_tmp matches ..8 run function modpack:leader/roll
execute if score #type ld_tmp = #last ld_last run scoreboard players operation #type ld_tmp %= #6 ld_tmp
execute if score #type ld_tmp = #last ld_last run scoreboard players add #type ld_tmp 1
""", total=total, ranges="\n".join(ranges))
    # note: when #last is 6, "%= 6" gives 0 and +1 gives 1; for 1..5 it gives the same value +1.
    fn("spawn_type", "\n".join(f"execute if score #type ld_tmp matches {STYLE[t]['n']} run function modpack:leader/summon/{t}"
                               for t in order))

    for t in order:
        d, s = Ty[t], STYLE[t]
        attrs = [f'{{Name:"minecraft:generic.max_health",Base:{num(d["hp"])}d}}',
                 f'{{Name:"minecraft:generic.movement_speed",Base:{num(d["speed"])}d}}',
                 f'{{Name:"minecraft:generic.attack_damage",Base:{num(d["damage"])}d}}',
                 f'{{Name:"minecraft:generic.follow_range",Base:{C["follow_range_normal"]}d}}']
        gear = ""
        if t == "brecher":
            attrs += [f'{{Name:"minecraft:generic.armor",Base:{num(d["armor"])}d}}',
                      f'{{Name:"minecraft:generic.armor_toughness",Base:{num(d["toughness"])}d}}',
                      f'{{Name:"minecraft:generic.knockback_resistance",Base:{num(d["knockback_res"])}d}}']
            gear = (',ArmorItems:[{},{id:"minecraft:iron_leggings",Count:1b},{id:"minecraft:iron_chestplate",Count:1b},'
                    '{id:"minecraft:iron_helmet",Count:1b}],HandItems:[{},{id:"minecraft:shield",Count:1b}]')
        nbt = (f'{{Tags:["modpack_horde_leader","leader_{t}","modpack_boss","ld_new"],PersistenceRequired:1b,IsBaby:0b,'
               f'CustomName:\'{{"text":"{d["name"]}","color":"{s["team"]}","bold":true}}\','
               f'DeathLootTable:"modpack:leaders/{t}",Health:{num(d["hp"])}f,Attributes:[{",".join(attrs)}]{gear},'
               f'HandDropChances:[0f,0f],ArmorDropChances:[0f,0f,0f,0f]}}')
        fn(f"summon/{t}", """
summon $ent ~ ~ ~ $nbt
execute as @e[tag=ld_new,limit=1,sort=nearest,distance=..3] at @s run function modpack:leader/setup/$t
""", ent=d["entity"], nbt=nbt, t=t)
        extra = []
        if t != "kriecher":
            extra.append("effect give @s minecraft:glowing infinite 0 true")
        if t == "brecher":
            extra.append(f"scale set pehkui:base {num(d['scale'])} @s")
        if t in ("kriecher", "platzer"):
            extra.append(f"scale set pehkui:width {num(d['width'])} @s")
            extra.append(f"scale set pehkui:height {num(d['height'])} @s")
        fn(f"setup/{t}", """
# As the new $name leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type $n
team join ld_$t @s
$extra
execute store result bossbar modpack:leader_$t max run data get entity @s Health
function modpack:leader/init
""", name=d["name"], n=s["n"], t=t, extra="\n".join(extra))
    fn("init", """
# As a new leader, at it: id, timers, daytime cap, link marker.
scoreboard players add #next ld_id 1
scoreboard players operation @s ld_id = #next ld_id
scoreboard players set @s ld_age 0
scoreboard players set @s ld_t 0
scoreboard players set @s ld_sum 0
scoreboard players set @s ld_cue 0
execute if score #day mh_tmp matches 1 unless data entity @s ArmorItems[3].id run item replace entity @s armor.head with minecraft:leather_helmet{Unbreakable:1b}
function modpack:leader/make_link
""")
    fn("make_link", """
# As + at a leader: a marker that follows it every tick and notices when it is gone.
summon minecraft:marker ~ ~ ~ {Tags:["ld_link","ld_newlink"]}
scoreboard players operation @e[type=minecraft:marker,tag=ld_newlink,distance=..1,limit=1] ld_id = @s ld_id
scoreboard players operation @e[type=minecraft:marker,tag=ld_newlink,distance=..1,limit=1] ld_type = @s ld_type
tag @e[type=minecraft:marker,tag=ld_newlink] remove ld_newlink
""")

    # ---------------- per-leader tick
    bar = []
    for t in order:
        n = STYLE[t]["n"]
        bar += [f"execute if score @s ld_type matches {n} run bossbar set modpack:leader_{t} players @a[distance=..{C['bossbar_range']}]",
                f"execute if score @s ld_type matches {n} store result bossbar modpack:leader_{t} value run scoreboard players get @s ld_hp",
                f"execute if score @s ld_type matches {n} run bossbar set modpack:leader_{t} visible true"]
    cue = [f"execute if score @s ld_type matches {STYLE[t]['n']} run playsound {STYLE[t]['cue'][0]} hostile "
           f"@a[distance=..{C['cue_range']}] ~ ~ ~ 2 {num(STYLE[t]['cue'][1])}" for t in order]
    aura = [f"execute if score @s ld_type matches {STYLE[t]['n']} run particle minecraft:dust {STYLE[t]['dust']} 1.2 "
            f"~ ~1 ~ 0.35 0.6 0.35 0 3" for t in order if t != "kriecher"]
    ai = [f"execute if score @s ld_type matches {STYLE[t]['n']} run function modpack:leader/ai/{t}"
          for t in ("laeufer", "spucker", "schreier", "kriecher")]
    fn("leader_tick", """
# Every 5 ticks, as + at a loaded leader.
execute store result score @s ld_hp run data get entity @s Health
$bar
scoreboard players operation #id ld_tmp = @s ld_id
scoreboard players set #hl ld_tmp 0
execute as @e[type=minecraft:marker,tag=ld_link,distance=..64] if score @s ld_id = #id ld_tmp run scoreboard players set #hl ld_tmp 1
execute if score #hl ld_tmp matches 0 run function modpack:leader/make_link
scoreboard players remove @s[scores={ld_cue=1..}] ld_cue 5
execute if score @s ld_cue matches ..0 if entity @a[distance=..$cr,gamemode=!spectator] run function modpack:leader/cue
$aura
$ai
execute if entity @a[distance=..$dr,gamemode=!spectator] run scoreboard players set @s ld_age 0
execute unless entity @a[distance=..$dr,gamemode=!spectator] run scoreboard players add @s ld_age 5
execute if score @s ld_age matches $dt.. run function modpack:leader/despawn
""", bar="\n".join(bar), cr=C["cue_range"], aura="\n".join(aura), ai="\n".join(ai),
       dr=C["despawn_player_range"], dt=tick(C["despawn_after_s"]))
    fn("cue", """
scoreboard players set @s ld_cue $cd
$cue
""", cd=tick(C["cue_cooldown_s"]), cue="\n".join(cue))

    # ---------------- type behaviour
    L = Ty["laeufer"]
    fn("ai/laeufer", """
# Sprints while it has a target (needs line of sight to acquire one) within $r blocks.
scoreboard players set #t ld_tmp 0
execute on target if entity @s[distance=..$r] run scoreboard players set #t ld_tmp 1
execute if score #t ld_tmp matches 1 run effect give @s minecraft:speed 1 $amp true
execute if score #t ld_tmp matches 1 run particle minecraft:cloud ~ ~0.2 ~ 0.2 0 0.2 0.01 2
""", r=L["sprint_range"], amp=L["sprint_amplifier"])

    S = Ty["spucker"]
    fn("ai/spucker", """
# Spits every $every_s s at the nearest player $mn-$mx blocks away; backs off from players closer than $rb.
scoreboard players add @s ld_t 5
execute if score @s ld_t matches $every.. if entity @p[distance=$mn..$mx,gamemode=!spectator] run function modpack:leader/spit
execute if entity @p[distance=..$rb,gamemode=!spectator] facing entity @p[distance=..$rb,gamemode=!spectator] feet rotated ~ 0 if block ^ ^ ^-1 #elytra_hordes:horde_air if block ^ ^1 ^-1 #elytra_hordes:horde_air run tp @s ^ ^ ^-$step
""", every_s=num(S["spit_every_s"]), every=tick(S["spit_every_s"]), mn=S["spit_min"], mx=S["spit_max"],
       rb=S["retreat_below"], step=num(S["retreat_step"]))
    fn("spit", """
scoreboard players set @s ld_t 0
playsound minecraft:entity.llama.spit hostile @a[distance=..32] ~ ~ ~ 1.5 0.6
execute anchored eyes positioned ^ ^ ^ facing entity @p[distance=..$mx,gamemode=!spectator] eyes run function modpack:leader/spit_throw
""", mx=S["spit_max"])
    lift = int(round(S["spit_lift"] * 1000 / S["spit_speed"]))
    fn("spit_throw", """
# At the Spucker's eyes, facing the target: a splash potion of Poison thrown along the view line with some lift.
summon minecraft:potion ^ ^ ^1 {Tags:["ld_spit_new"],Item:{id:"minecraft:splash_potion",Count:1b,tag:{CustomPotionColor:7516192,CustomPotionEffects:[{Id:19,Amplifier:${pamp}b,Duration:$pdur}]}}}
summon minecraft:marker ^ ^ ^ {Tags:["ld_d0"]}
summon minecraft:marker ^ ^ ^1 {Tags:["ld_d1"]}
execute store result score #x0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[0] 1000
execute store result score #y0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[1] 1000
execute store result score #z0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[2] 1000
execute store result score #x1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[0] 1000
execute store result score #y1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[1] 1000
execute store result score #z1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[2] 1000
scoreboard players operation #x1 ld_tmp -= #x0 ld_tmp
scoreboard players operation #y1 ld_tmp -= #y0 ld_tmp
scoreboard players operation #z1 ld_tmp -= #z0 ld_tmp
scoreboard players add #y1 ld_tmp $lift
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[0] double $scale run scoreboard players get #x1 ld_tmp
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[1] double $scale run scoreboard players get #y1 ld_tmp
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[2] double $scale run scoreboard players get #z1 ld_tmp
kill @e[type=minecraft:marker,tag=ld_d0]
kill @e[type=minecraft:marker,tag=ld_d1]
tag @e[type=minecraft:potion,tag=ld_spit_new] remove ld_spit_new
""", pamp=S["poison_amplifier"], pdur=tick(S["poison_s"]), lift=lift, scale=num(S["spit_speed"] / 1000))

    R = Ty["schreier"]
    supp_terms = [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"equipment": {"mainhand": {
        "items": ["tacz:modern_kinetic_gun"],
        "nbt": '{AttachmentMUZZLE:{tag:{AttachmentId:"tacz:muzzle_silencer_%s"}}}' % s}}}} for s in SILENCERS]
    js("data/modpack/predicates/leader/suppressed.json", {"condition": "minecraft:any_of", "terms": supp_terms})
    fn("ai/schreier", """
# Screams every $every_s s (while a player is within $sr blocks) and calls $k zombies, at most $cap in total.
# Unsuppressed gunfire within $sr blocks makes it scream sooner.
scoreboard players add @s ld_t 5
execute if entity @a[distance=..$sr,scores={mh_gun=1..},predicate=!modpack:leader/suppressed] run scoreboard players add @s ld_t $speedup
execute if score @s ld_t matches $every.. if score @s ld_sum matches ..$capm1 if entity @a[distance=..$sr,gamemode=!spectator] run function modpack:leader/scream
""", every_s=num(R["scream_every_s"]), every=tick(R["scream_every_s"]), sr=R["scream_range"], k=R["zombies_per_scream"],
       cap=R["zombie_cap"], capm1=R["zombie_cap"] - 1, speedup=tick(R["gunfire_speedup_s"]))
    called = "\n".join(
        f'summon minecraft:zombie ~{dx} ~ ~{dz} {{Tags:["modpack_horde","ld_called"],PersistenceRequired:1b,'
        f'Attributes:[{{Name:"minecraft:generic.follow_range",Base:{C["follow_range_normal"]}d}}]}}'
        for dx, dz in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2)][:R["zombies_per_scream"]])
    fn("scream", """
scoreboard players set @s ld_t 0
scoreboard players add @s ld_sum $k
playsound minecraft:entity.ghast.scream hostile @a[distance=..64] ~ ~ ~ 3 0.6
particle minecraft:angry_villager ~ ~2 ~ 0.6 0.4 0.6 0 8
title @a[distance=..$sr] actionbar {"text":"The Schreier screams for the horde!","color":"light_purple"}
$called
""", k=R["zombies_per_scream"], sr=R["scream_range"], called=called)

    K = Ty["kriecher"]
    js("data/modpack/predicates/leader/lit.json",
       {"condition": "minecraft:location_check", "predicate": {"light": {"light": {"min": K["light_min"]}}}})
    fn("ai/kriecher", """
# Invisible in the dark, glowing and with an aura in light (light level >= $lm at its feet).
execute if predicate modpack:leader/lit run function modpack:leader/kriecher_lit
execute unless predicate modpack:leader/lit run effect give @s minecraft:invisibility 1 0 true
""", lm=K["light_min"])
    fn("kriecher_lit", """
effect clear @s minecraft:invisibility
effect give @s minecraft:glowing 1 0 true
particle minecraft:dust $dust 1.2 ~ ~0.4 ~ 0.4 0.2 0.4 0 3
""", dust=STYLE["kriecher"]["dust"])
    fn("kriecher_grab", """
# Advancement reward, as a player the Kriecher just hit: legs grabbed.
effect give @s minecraft:slowness $s $amp true
playsound minecraft:entity.spider.ambient hostile @s ~ ~ ~ 1 0.5
title @s actionbar {"text":"Something grabs your legs!","color":"aqua"}
advancement revoke @s only modpack:leaders/kriecher_grab
""", s=K["grab_slow_s"], amp=K["grab_slow_amplifier"])
    js("data/modpack/advancements/leaders/kriecher_grab.json", {
        "criteria": {"grab": {"trigger": "minecraft:entity_hurt_player", "conditions": {"damage": {
            "source_entity": {"nbt": '{Tags:["leader_kriecher"]}'}}}}},
        "rewards": {"function": "modpack:leader/kriecher_grab"}})

    P = Ty["platzer"]
    grief = "summon minecraft:creeper ~ ~ ~ {Fuse:0,ignited:1b,ExplosionRadius:2b}" if P["grief_blocks"] else \
        "# grief_blocks is off: no block damage"
    fn("platzer_blast", """
# At the spot where a Platzer died. Damage (minecraft:explosion, so armour and Blast Protection count) to
# players and to every hostile mob (horde included); no block damage unless grief_blocks is on.
particle minecraft:explosion ~ ~1 ~ 1.2 0.8 1.2 0 8 force
particle minecraft:dust 0.4 0.8 0.2 2 ~ ~1 ~ 2 1 2 0 60 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 0.9
execute as @a[distance=..$ri,gamemode=!creative,gamemode=!spectator] run damage @s $di minecraft:explosion
execute as @a[distance=$ri..$ro,gamemode=!creative,gamemode=!spectator] run damage @s $do minecraft:explosion
execute as @e[type=#elytra_hordes:hostiles,distance=..$ro] run damage @s $di minecraft:explosion
$grief
""", ri=num(P["blast_inner"]), ro=num(P["blast_outer"]), di=num(P["damage_inner"]), do=num(P["damage_outer"]),
       grief=grief)

    # ---------------- death, despawn, horde break
    hide = "\n".join(f"execute if score @s ld_type matches {STYLE[t]['n']} run bossbar set modpack:leader_{t} visible false"
                     for t in order)
    fn("link_check", """
# As + at a link marker: is its leader still alive? (Health read x10; 0 = dead or gone.)
scoreboard players operation #id ld_tmp = @s ld_id
scoreboard players set #h ld_tmp 0
execute as @e[tag=modpack_horde_leader,distance=..64] if score @s ld_id = #id ld_tmp store result score #h ld_tmp run data get entity @s Health 10
execute if score #h ld_tmp matches ..0 run function modpack:leader/died
""")
    fn("died", """
# As + at the link of a leader that is gone. With a player near it was killed (effects run);
# otherwise it was only unloaded or removed, so it is cleaned up quietly.
execute if entity @a[distance=..64,gamemode=!spectator] run function modpack:leader/on_death
function modpack:leader/unlink
""")
    fn("on_death", """
execute if score @s ld_type matches 6 run function modpack:leader/platzer_blast
function modpack:leader/break
title @a[distance=..48] actionbar {"text":"The leader has fallen. The horde scatters!","color":"gold"}
""")
    fn("break", """
# Horde zombies near the dead leader lose their target for $bs s, the lure towards players stops.
execute as @e[type=#elytra_hordes:horde_types,tag=modpack_horde,distance=..$br] run function modpack:leader/break_one
scoreboard players reset @a[distance=..96] mh_lure
kill @e[type=#elytra_hordes:za_senses,tag=mh_lure_sense,distance=..96]
""", bs=C["break_seconds"], br=C["break_radius"])
    fn("break_one", """
attribute @s minecraft:generic.follow_range base set 0
effect give @s minecraft:slowness $bs 1 true
tag @s add ld_broken
scoreboard players set @s ld_brk $loops
""", bs=C["break_seconds"], loops=C["break_seconds"] * 4)
    fn("broken_tick", """
scoreboard players remove @s ld_brk 1
execute if score @s ld_brk matches ..0 run function modpack:leader/unbreak
""")
    fn("unbreak", """
attribute @s minecraft:generic.follow_range base set $fr
tag @s remove ld_broken
""", fr=C["follow_range_normal"])
    fn("unlink", """
$hide
kill @s
""", hide=hide)
    fn("despawn", """
# As + at a leader: removed without drops and without death effects.
scoreboard players operation #id ld_tmp = @s ld_id
execute as @e[type=minecraft:marker,tag=ld_link] if score @s ld_id = #id ld_tmp run function modpack:leader/unlink
data merge entity @s {DeathLootTable:"minecraft:empty"}
tp @s ~ -2000 ~
kill @s
""")
    allhide = "\n".join(f"bossbar set modpack:leader_{t} visible false" for t in order)
    fn("clear", """
# TEST/CLEANUP: /function modpack:leader/clear removes every loaded leader (no drops, no explosion).
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/despawn
kill @e[type=minecraft:marker,tag=ld_link]
$allhide
""", allhide=allhide)
    fn("status", """
execute store result score #n ld_tmp if entity @e[tag=modpack_horde_leader]
tellraw @s [{"text":"[Leaders] last type: ","color":"gold"},{"score":{"name":"#last","objective":"ld_last"}},{"text":" (1 Läufer, 2 Brecher, 3 Spucker, 4 Schreier, 5 Kriecher, 6 Platzer) | loaded leaders: "},{"score":{"name":"#n","objective":"ld_tmp"}}]
""")
    for t in order:
        n = STYLE[t]["n"]
        fn(f"force/{t}", """
# TEST: /function modpack:leader/force/$t  (as a player, overworld): a horde led by a $name, now.
scoreboard players set #force ld_tmp $n
function modpack:horde/start
scoreboard players set #force ld_tmp 0
""", t=t, n=n, name=Ty[t]["name"])
        fn(f"here/{t}", """
# TEST: /function modpack:leader/here/$t  a lone $name 6 blocks in front of you (no horde, ignores caps).
scoreboard players set #day mh_tmp 0
scoreboard players set #type ld_tmp $n
scoreboard players operation #last ld_last = #type ld_tmp
scoreboard players set #up ld_tmp 0
execute rotated ~ 0 positioned ^ ^ ^6 align xz positioned ~0.5 ~ ~0.5 run function modpack:leader/here_find/$t
""", t=t, n=n, name=Ty[t]["name"])
        fn(f"here_find/{t}", """
# Steps up (max 24 blocks) until there are 3 free blocks, then summons there (feet on the ground below).
execute if block ~ ~ ~ #elytra_hordes:horde_air if block ~ ~1 ~ #elytra_hordes:horde_air if block ~ ~2 ~ #elytra_hordes:horde_air run function modpack:leader/summon/$t
execute if block ~ ~ ~ #elytra_hordes:horde_air if block ~ ~1 ~ #elytra_hordes:horde_air if block ~ ~2 ~ #elytra_hordes:horde_air run scoreboard players set #up ld_tmp 99
scoreboard players add #up ld_tmp 1
execute if score #up ld_tmp matches ..24 positioned ~ ~1 ~ run function modpack:leader/here_find/$t
""", t=t)

    # ---------------- loot, advancements
    for t, pools in loot_tables().items():
        for p in pools:
            check_items(p["entries"])
        js(f"data/modpack/loot_tables/leaders/{t}.json", {"type": "minecraft:entity", "pools": pools})
    js("data/modpack/advancements/leaders/root.json", {
        "display": {"icon": {"item": "minecraft:zombie_head"}, "title": {"text": "Horde Leaders"},
                    "description": {"text": "Every horde has someone in charge"},
                    "background": "minecraft:textures/block/coarse_dirt.png", "frame": "task",
                    "show_toast": False, "announce_to_chat": False, "hidden": False},
        "criteria": {"tick": {"trigger": "minecraft:tick"}}})

    def kill_adv(key, tag, title, desc, icon, frame="goal"):
        js(f"data/modpack/advancements/leaders/{key}.json", {
            "parent": "modpack:leaders/root",
            "display": {"icon": {"item": icon}, "title": {"text": title}, "description": {"text": desc},
                        "frame": frame, "show_toast": True, "announce_to_chat": True, "hidden": False},
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"nbt": '{Tags:["%s"]}' % tag}}]}}}})
    kill_adv("kill_any", "modpack_horde_leader", "Cut Off the Head", "Kill any horde leader", "minecraft:zombie_head", "task")
    icons = {"laeufer": "minecraft:sugar", "brecher": "minecraft:iron_chestplate", "spucker": "minecraft:spider_eye",
             "schreier": "minecraft:goat_horn", "kriecher": "minecraft:torch", "platzer": "minecraft:tnt"}
    for t in order:
        kill_adv(f"kill_{t}", f"leader_{t}", f"{Ty[t]['name']} Down", f"Kill a {Ty[t]['name']} horde leader", icons[t])

    files["README_leaders.md"] = README.strip() + "\n"
    return files


README = """
# Horde leaders (generated by questtools/leadergen.py)

Every horde is led by ONE mini-boss. **All numbers live in CONFIG at the top of `questtools/leadergen.py`.**
Edit there, run `py leadergen.py`, then `/reload`. Do not edit the files in `data/modpack/functions/leader/`;
they are rewritten on every run.

| Type (id) | Entity | Behaviour | Counter | Glow |
|---|---|---|---|---|
| Läufer (1) | zombie | Speed III while it has a target within 24 blocks; low health | shotgun | yellow |
| Brecher (2) | zombie, Pehkui 1.25x | armour 30 + toughness 20 (vanilla max), no knockback, slow | high armor_ignore guns, FMJ/Slug ammo mods, headshots | red |
| Spucker (3) | husk | throws Poison splash potions at 8-24 blocks every 3 s, backs away from players closer than 8 | sniper rifle | green |
| Schreier (4) | zombie villager | screams every 15 s, calls 2 zombies (max 6); unsuppressed gunfire nearby speeds it up | suppressor, kill first | purple |
| Kriecher (5) | zombie, Pehkui squat | invisible in the dark, glows in light (level 8+); a hit gives Slowness III | light up the area, melee | aqua |
| Platzer (6) | drowned, Pehkui bloated | on death: explosion damage to players and hostile mobs (14 / 6), no block damage | keep distance | gold |

Weights: Läufer 30, Spucker 20, Kriecher 15, Platzer 15, Brecher 10, Schreier 10; never the same type twice in a row.

## Test commands
- `/function modpack:leader/force/<type>` a horde with that leader (laeufer, brecher, spucker, schreier, kriecher, platzer)
- `/function modpack:leader/here/<type>` one leader 6 blocks in front of you, no horde
- `/function modpack:leader/clear` remove all leaders (no drops, no explosion)
- `/function modpack:leader/status` or `/scoreboard players get #last ld_last` last leader type
"""


# =============================================================================== skins (resource pack)
# Needs the client mod Entity Texture Features: it swaps a mob's texture by its custom name, so only the
# leaders change (normal zombies keep the vanilla look). Without ETF the leaders just look vanilla.
RP = os.path.join(gamedata.MC_DIR, "config", "paxi", "resourcepacks", "elytra_leaders_rp")
# base texture (under textures/entity/) per entity, its "skin" hue range, and the 4 eye pixels
BASES = {
    "minecraft:zombie": ("zombie/zombie", (0.17, 0.42), [(9, 12), (10, 12), (13, 12), (14, 12)]),
    "minecraft:husk": ("zombie/husk", (0.05, 0.17), [(9, 12), (10, 12), (13, 12), (14, 12)]),
    "minecraft:drowned": ("zombie/drowned", (0.40, 0.55), [(9, 12), (10, 12), (13, 12), (14, 12)]),
    "minecraft:zombie_villager": ("zombie_villager/zombie_villager", (0.17, 0.42), [(9, 14), (10, 14), (13, 14), (14, 14)]),
}
# per type: (skin hue, saturation, brightness factor), (clothes hue, saturation, brightness factor)
PALETTE = {
    "laeufer": ((0.16, 0.35, 1.10), (0.00, 0.00, 0.75)),   # pale yellowish skin, grey rags
    "brecher": ((0.04, 0.55, 0.85), (0.60, 0.12, 0.70)),   # rusty skin, dark iron cloth
    "spucker": ((0.27, 0.65, 1.00), (0.12, 0.55, 0.80)),   # sickly green skin, mustard rags
    "schreier": ((0.80, 0.35, 0.95), (0.75, 0.30, 0.55)),  # purple skin, dark robe
    "kriecher": ((0.55, 0.15, 0.55), (0.00, 0.00, 0.40)),  # dark slate skin, black clothes
    "platzer": ((0.08, 0.70, 1.75), (0.07, 0.45, 0.95)),   # swollen orange skin, brown rags
}


def _tint(px, skin_range, skin, cloth):
    import colorsys
    out = []
    for r, g, b, a in px:
        if a == 0:
            out.append((r, g, b, a))
            continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        th, ts, tv = skin if (skin_range[0] <= h <= skin_range[1] and s > 0.15) else cloth
        nr, ng, nb = colorsys.hsv_to_rgb(th, ts, min(1.0, v * tv))
        out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
    return out


def skins():
    import zipfile
    import pngtool
    files = {"pack.mcmeta": json.dumps({"pack": {"pack_format": 15, "description":
                                                 "Elytra modpack horde leader skins (needs Entity Texture Features)"}},
                                       indent=2) + "\n"}
    by_base = {}
    for t, d in CONFIG["types"].items():
        by_base.setdefault(d["entity"], []).append(t)
    with zipfile.ZipFile(gamedata._client_jar()) as z:
        for ent, types in by_base.items():
            base, rng, eyes = BASES[ent]
            folder, name = base.rsplit("/", 1)
            w, h, px = pngtool.read(z.read(f"assets/minecraft/textures/entity/{base}.png"))
            props = []
            for i, t in enumerate(types, start=1):
                var = i + 1
                skin, cloth = PALETTE[t]
                new = _tint(px, rng, skin, cloth)
                glow = tuple(round(float(c) * 255) for c in STYLE[t]["dust"].split()) + (255,)
                emis = [(0, 0, 0, 0)] * (w * h)
                for x, y in eyes:
                    new[y * w + x] = glow
                    emis[y * w + x] = glow
                d = f"assets/minecraft/optifine/random/entity/{folder}"
                files[f"{d}/{name}{var}.png"] = pngtool.write(w, h, new)
                files[f"{d}/{name}{var}_e.png"] = pngtool.write(w, h, emis)
                nm = CONFIG["types"][t]["name"]
                match = nm if nm.isascii() else "regex:" + "".join(c if c.isascii() else "." for c in nm)
                props += [f"textures.{i}={var}", f"name.{i}={match}"]
            files[f"assets/minecraft/optifine/random/entity/{folder}/{name}.properties"] = "\n".join(props) + "\n"
            if ent == "minecraft:drowned":   # the drowned's outer layer (rags) follows the same rules
                w2, h2, px2 = pngtool.read(z.read("assets/minecraft/textures/entity/zombie/drowned_outer_layer.png"))
                lp = []
                for i, t in enumerate(types, start=1):
                    files[f"assets/minecraft/optifine/random/entity/zombie/drowned_outer_layer{i + 1}.png"] = \
                        pngtool.write(w2, h2, _tint(px2, (2, 2), PALETTE[t][1], PALETTE[t][1]))
                    lp += [f"textures.{i}={i + 1}", f"name.{i}={CONFIG['types'][t]['name']}"]
                files["assets/minecraft/optifine/random/entity/zombie/drowned_outer_layer.properties"] = "\n".join(lp) + "\n"
    return files


def write_skins():
    files = skins()
    if os.path.exists(RP):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        shutil.copytree(RP, os.path.join(gamedata.INSTANCE, "backup", f"leaders-rp-{stamp}"))
        shutil.rmtree(RP)
    for rel, data in files.items():
        p = os.path.join(RP, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data if isinstance(data, bytes) else data.encode("utf-8"))
    return len(files)


# =============================================================================== hooks + write

def add_hooks():
    changed = []
    for tag, value in (("load", "modpack:leader/load"), ("tick", "modpack:leader/tick")):
        p = os.path.join(PACK, "data", "minecraft", "tags", "functions", f"{tag}.json")
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        if value not in d["values"]:
            d["values"].append(value)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                json.dump(d, f, indent=2)
            changed.append(f"{tag}.json")
    for name, after, line in (("spawn_horde", "function modpack:horde/spawn_member", "function modpack:leader/spawn"),
                              ("clear", None, "function modpack:leader/clear")):
        p = os.path.join(PACK, "data", "modpack", "functions", "horde", f"{name}.mcfunction")
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if line in text:
            continue
        if after:
            if after not in text:
                raise BuildError(f"horde/{name}: hook point '{after}' not found")
            text = text.replace(after, after + "\n" + line, 1)
        else:
            text = text.rstrip("\n") + "\n" + line + "\n"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        changed.append(f"horde/{name}.mcfunction")
    return changed


OWNED = ["data/modpack/functions/leader", "data/modpack/loot_tables/leaders", "data/modpack/advancements/leaders",
         "data/modpack/predicates/leader", "README_leaders.md"]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        files = build()
    except BuildError as e:
        print(f"ERROR: {e}")
        return 2
    print(f"Leader files: {len(files)}")
    if "--check" in argv:
        return 0
    if not os.path.isdir(PACK):
        print("ERROR: the elytra_hordes pack does not exist")
        return 2
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    bdir = os.path.join(gamedata.INSTANCE, "backup", f"leaders-{stamp}")
    for rel in OWNED:
        src = os.path.join(PACK, *rel.split("/"))
        if os.path.exists(src):
            dst = os.path.join(bdir, *rel.split("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
            (shutil.rmtree if os.path.isdir(src) else os.remove)(src)
    for rel, text in files.items():
        p = os.path.join(PACK, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:   # UTF-8 without BOM
            f.write(text)
    print(f"Wrote {write_skins()} files to config/paxi/resourcepacks/elytra_leaders_rp")
    hooks = add_hooks()
    print(f"Wrote {len(files)} files to elytra_hordes" + (f"; hooks added: {', '.join(hooks)}" if hooks else ""))
    if os.path.isdir(bdir):
        print(f"Previous leader files backed up to backup/leaders-{stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
