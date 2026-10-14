"""Phase 3 dungeons for dungeongen.py: the Storm Spire (sky tower) and the Hollow (own dimension).

Storm Spire   floating island + tower at y~225-257, reachable by elytra. Rocket resupply barrel on the
              landing pad. Boss: Tempest Herald (ghast). Weak point: a glowing Storm Core rides on him;
              his body has Resistance IV (takes 20%), hits on the core are passed on to him x3.
The Hollow    a void dimension (End sky). Reached through Rift Gates (ruined crying-obsidian frames in the
              overworld). Boss: Hollow Magus (evoker). Shield: immune while 4 end crystals stand on the
              pillars; shoot them all to drop the shield for 15 s (and get an ammo drop).
"""

import math
import random

from structlib import Template, ammo_entry, att_entry, check_items, gun_entry, item_entry, pool


def disc(t, cx, y, cz, r, block, skip=None):
    for x in range(int(cx - r) - 1, int(cx + r) + 2):
        for z in range(int(cz - r) - 1, int(cz + r) + 2):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                if 0 <= x < t.size[0] and 0 <= z < t.size[2] and not (skip and skip(x, z)):
                    t.set(x, y, z, block)


def boss_drop_tables(pack, ns, boss, guns):
    """guns: {gun_id: ammo_id}. Writes boss/guns/<gun> sub-tables, returns the weighted pool."""
    import gamedata
    for g, a in guns.items():
        stack = gamedata.load().ammo_stack("tacz:" + a)
        pack.json(f"data/{ns}/loot_tables/boss/guns/{g}.json",
                  {"type": "minecraft:chest", "pools": [pool([gun_entry(g)]), pool([ammo_entry(a, stack)])]})
    return pool([{"type": "minecraft:loot_table", "name": f"{ns}:boss/guns/{g}", "weight": 1} for g in guns])


def write_loot(pack, ns, name, pools):
    for p in pools:
        check_items(p["entries"])
    pack.json(f"data/{ns}/loot_tables/{name}.json", {"type": "minecraft:chest", "pools": pools})


def advancement(pack, ns, key, icon, title, desc):
    pack.json(f"data/{ns}/advancements/bosses/{key}.json", {
        "parent": f"{ns}:bosses/root",
        "display": {"icon": {"item": icon}, "title": {"text": title}, "description": {"text": desc},
                    "frame": "challenge", "show_toast": True, "announce_to_chat": True, "hidden": False},
        "criteria": {"defeated": {"trigger": "minecraft:impossible"}}})


# ============================================================================ STORM SPIRE

SS = "storm_spire"


def ss_template():
    rnd = random.Random(11)
    t = Template(31, 32, 31)
    c = 15
    # floating island: an upside-down cone, ragged at the edge
    for y in range(0, 8):
        r = 2 + y * 1.55
        for x in range(31):
            for z in range(31):
                d = math.hypot(x - c, z - c)
                if d > r:
                    continue
                if y < 6 and d > r - 1.2 and rnd.random() < 0.35:
                    continue
                if y == 7:
                    b = "moss_block" if rnd.random() < 0.15 else "grass_block[snowy=false]"
                elif y == 6:
                    b = "dirt"
                else:
                    b = rnd.choice(["stone", "stone", "andesite", "tuff", "cobblestone"])
                t.set(x, y, z, b)
    # landing pad + rocket resupply barrel (south)
    t.fill(12, 7, 23, 18, 7, 27, "stone_bricks")
    t.set(15, 8, 26, "barrel[facing=up,open=false]")
    t.entity(15, 8, 26, {"id": "minecraft:marker", "Tags": ["ed_resupply"]})
    for x in (12, 18):
        t.set(x, 8, 23, "stone_bricks")
        t.set(x, 9, 23, "lantern[hanging=false,waterlogged=false]")
    # tower
    t.hollow(11, 7, 11, 19, 27, 19, "calcite")
    t.fill(12, 7, 12, 18, 7, 18, "quartz_bricks")
    for x, z in ((11, 11), (19, 11), (11, 19), (19, 19)):
        t.fill(x, 8, z, x, 26, z, "quartz_pillar[axis=y]")
    for y1 in (12, 19):
        t.fill(11, y1, 15, 11, y1 + 2, 15, "light_blue_stained_glass")
        t.fill(19, y1, 15, 19, y1 + 2, 15, "light_blue_stained_glass")
        t.fill(15, y1, 11, 15, y1 + 2, 11, "light_blue_stained_glass")
    t.fill(14, 8, 19, 16, 10, 19, "air")                                # door
    t.fill(15, 8, 12, 15, 26, 12, "ladder[facing=south,waterlogged=false]")
    t.chest(12, 8, 12, "east", "elytra_dungeons:chests/storm_spire_tower")
    t.set(18, 8, 18, "lantern[hanging=false,waterlogged=false]")
    # arena platform on top
    disc(t, c, 27, c, 12, "smooth_quartz")
    for x in range(31):
        for z in range(31):
            d = math.hypot(x - c, z - c)
            if 11 <= d <= 12.2 and t.get(x, 27, z):
                t.set(x, 27, z, "waxed_oxidized_cut_copper")
    for dx, dz in ((6, 0), (-6, 0), (0, 6), (0, -6), (4, 4), (-4, 4), (4, -4), (-4, -4)):
        t.set(c + dx, 27, c + dz, "sea_lantern")
    t.set(c, 27, c, "chiseled_quartz_block")
    t.set(15, 27, 12, "air")                                            # ladder hatch
    for dx, dz in ((9, 0), (-9, 0), (0, 9), (0, -9)):                   # lightning pylons
        t.fill(c + dx, 28, c + dz, c + dx, 30, c + dz, "waxed_oxidized_cut_copper")
        t.set(c + dx, 31, c + dz, "lightning_rod[facing=up,powered=false,waterlogged=false]")
    t.entity(c, 28, c, {"id": "minecraft:marker", "Tags": ["ed_arena", "ed_spire", "ed_idle"]})
    return t


def crown_template():
    """Tempest Crown (v2 Storm Spire): 47 x 17 x 47. Floating island, a 39-wide sky arena on top (y=9),
    low rim with 4 openings, 8 lightning-rod columns at the edge, south landing dock with the rocket
    barrel, and a small vault inside the island under a trapdoor."""
    rnd = random.Random(23)
    t = Template(47, 17, 47)
    c = 23
    for y in range(0, 9):                                               # island
        r = 3 + y * 2.1
        for x in range(47):
            for z in range(47):
                d = math.hypot(x - c, z - c)
                if d > r or (y < 8 and d > r - 1.5 and rnd.random() < 0.35):
                    continue
                t.set(x, y, z, rnd.choice(["stone", "stone", "andesite", "calcite", "tuff"]))
    for x in range(47):                                                 # roots hanging under the edges
        for z in range(47):
            for y in range(1, 9):
                if t.get(x, y, z) and not t.get(x, y - 1, z):
                    if rnd.random() < 0.12:
                        t.set(x, y - 1, z, "hanging_roots[waterlogged=false]")
                    break
    # vault inside the island
    t.fill(20, 4, 20, 26, 4, 26, "polished_deepslate")
    t.fill(20, 5, 20, 26, 8, 26, "air")
    t.chest(20, 5, 20, "east", "elytra_dungeons:chests/storm_spire_tower")
    t.set(26, 5, 20, "lantern[hanging=false,waterlogged=false]")
    t.set(20, 5, 25, "lantern[hanging=false,waterlogged=false]")
    t.fill(23, 5, 26, 23, 8, 26, "ladder[facing=north,waterlogged=false]")
    # arena floor
    for x in range(47):
        for z in range(47):
            d = math.hypot(x - c, z - c)
            if d > 19.4:
                continue
            if d >= 17.6:
                b = "polished_deepslate"
            elif 9.5 <= d <= 10.5:
                b = "waxed_oxidized_cut_copper"
            elif d <= 2.5:
                b = "chiseled_quartz_block"
            elif abs(abs(x - c) - abs(z - c)) == 0 and 3 <= d <= 9:
                b = "cyan_terracotta"
            else:
                b = "calcite"
            t.set(x, 9, z, b)
            if 18.6 <= d <= 19.4 and abs(x - c) > 2 and abs(z - c) > 2:
                t.set(x, 10, z, "smooth_quartz_slab[type=bottom,waterlogged=false]")
    for dx, dz in ((13, 0), (-13, 0), (0, 13), (0, -13)):
        t.set(c + dx, 9, c + dz, "sea_lantern")
    t.set(23, 9, 26, "spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    for ang in (20, 70, 110, 160, 200, 250, 290, 340):                 # lightning columns at the rim
        x = round(c + 16.5 * math.cos(math.radians(ang)))
        z = round(c + 16.5 * math.sin(math.radians(ang)))
        t.fill(x, 10, z, x, 14, z, "quartz_pillar[axis=y]")
        t.set(x, 15, z, "waxed_oxidized_cut_copper")
        t.set(x, 16, z, "lightning_rod[facing=up,powered=false,waterlogged=false]")
    # landing dock (south) with the rocket resupply barrel
    t.fill(21, 9, 42, 25, 9, 46, "stone_bricks")
    t.fill(21, 8, 42, 25, 8, 44, "stone_bricks")
    t.set(23, 10, 45, "barrel[facing=up,open=false]")
    t.entity(23, 10, 45, {"id": "minecraft:marker", "Tags": ["ed_resupply"]})
    wall = "stone_brick_wall[east=none,north=none,south=none,west=none,up=true,waterlogged=false]"
    for x in (21, 25):
        t.set(x, 10, 46, wall)
        t.set(x, 11, 46, "lantern[hanging=false,waterlogged=false]")
    t.entity(c, 10, c, {"id": "minecraft:marker", "Tags": ["ed_arena", "ed_spire", "ed_idle"]})
    return t


def storm_spire(pack, ns, template_pool):
    pack.template(f"{SS}/spire", ss_template())       # v1, kept so spires generated before the redesign still load
    pack.template(f"{SS}/crown", crown_template())
    template_pool(pack, f"{SS}/start", [(f"{SS}/crown", 1)], "minecraft:empty")
    pack.json(f"data/{ns}/tags/worldgen/biome/has_structure/{SS}.json", {"values": [
        "#minecraft:is_ocean", "#minecraft:is_forest", "#minecraft:is_taiga", "#minecraft:is_jungle",
        "#minecraft:is_savanna", "#minecraft:is_beach", "#minecraft:is_river", "minecraft:plains",
        "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:desert", "minecraft:swamp",
        "minecraft:snowy_plains", "minecraft:mushroom_fields"]})
    pack.json(f"data/{ns}/worldgen/structure/{SS}.json", {
        "type": "minecraft:jigsaw", "biomes": f"#{ns}:has_structure/{SS}", "max_distance_from_center": 80,
        "size": 1, "spawn_overrides": {}, "start_height": {"absolute": 225}, "start_pool": f"{ns}:{SS}/start",
        "step": "surface_structures", "terrain_adaptation": "none", "use_expansion_hack": False})
    pack.json(f"data/{ns}/worldgen/structure_set/{SS}.json", {
        "placement": {"type": "minecraft:random_spread", "salt": 552019877, "separation": 28, "spacing": 72},
        "structures": [{"structure": f"{ns}:{SS}", "weight": 1}]})

    F = f"{ns}:{SS}"
    BAR = f"{ns}:tempest_herald"
    core_nbt = ('{Size:1,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,Health:1000f,'
                'Attributes:[{Name:"minecraft:generic.max_health",Base:1000d}],Tags:["ed_herald_core"%s],'
                'CustomName:\'{"text":"Storm Ruby","color":"red","bold":true}\'}')
    visual = ('{Tags:["ed_herald_vis"],item:{id:"minecraft:paper",Count:1b,tag:{CustomModelData:7101}},'
              'item_display:"none",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
              'translation:[0f,0f,0f],scale:[4f,4f,4f]},view_range:2f}')
    herald = ('{Tags:["ed_herald_boss","ed_boss"],CustomName:\'{"text":"Tempest Herald","color":"aqua","bold":true}\','
              'CustomNameVisible:1b,PersistenceRequired:1b,NoAI:1b,Health:400f,'
              'Attributes:[{Name:"minecraft:generic.max_health",Base:400d}]}')
    rider = '{Tags:["ed_add","ed_herald_add"],PersistenceRequired:1b,CustomName:\'{"text":"Storm Rider","color":"gray"}\'}'
    fireball = '{Tags:["ed_fb_new","ed_herald_fb"],ExplosionPower:0,power:[0.0d,0.0d,0.0d]}'

    pack.function(f"{SS}/arena_tick", f"""
execute if entity @s[tag=ed_idle] if entity @a[distance=..20,gamemode=!spectator] run function {F}/start
execute if entity @s[tag=ed_active] run function {F}/active
""")
    pack.function(f"{SS}/start", f"""
tag @s remove ed_idle
tag @s add ed_active
scoreboard players set @s ed_angle 0
summon minecraft:ghast ~ ~11 ~10 {herald}
summon minecraft:slime ~ ~15.5 ~10 {core_nbt % ""}
summon minecraft:item_display ~ ~13 ~10 {visual}
effect give @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] minecraft:resistance infinite 3 true
effect give @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] minecraft:invisibility infinite 0 true
effect give @e[type=minecraft:slime,tag=ed_herald_core,distance=..24] minecraft:invisibility infinite 0 true
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_phase 1
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_wave 100
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_fb 0
bossbar set {BAR} players @a[distance=..64]
bossbar set {BAR} value 400
bossbar set {BAR} visible true
title @a[distance=..64] title {{"text":"The Tempest Herald","color":"aqua","bold":true}}
title @a[distance=..64] subtitle {{"text":"shoot the ruby on his forehead","color":"gray"}}
playsound minecraft:entity.ghast.scream hostile @a[distance=..64] ~ ~ ~ 2 0.5
""")
    pack.function(f"{SS}/fly", f"""
# every tick while the fight runs (as + at the arena marker): the Herald circles 10 blocks out, 11 up,
# always facing the nearest player; the core floats above his head; aimed fireballs on a timer
scoreboard players add @s ed_angle 2
execute if entity @e[type=minecraft:ghast,tag=ed_herald_boss,scores={{ed_phase=2..}},distance=..64] run scoreboard players add @s ed_angle 1
execute if score @s ed_angle matches 360.. run scoreboard players remove @s ed_angle 360
execute store result entity @s Rotation[0] float 1 run scoreboard players get @s ed_angle
execute rotated as @s positioned ^ ^11 ^10 as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..64,limit=1] run tp @s ~ ~ ~ facing entity @p[gamemode=!spectator] eyes
execute as @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..80] at @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..80,limit=1] run tp @s ~ ~2 ~ ~ 0
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80] at @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..80,limit=1] rotated ~ 0 positioned ~ ~2 ~ positioned ^ ^1.25 ^2.35 run tp @s ~ ~-0.52 ~
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80] at @s run particle minecraft:dust 1.0 0.1 0.15 1.2 ~ ~0.52 ~ 0.25 0.25 0.25 0 2
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80,limit=1] run function {F}/core_tick
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..64,limit=1] run function {F}/fire_timer
""")
    pack.function(f"{SS}/fire_timer", f"""
# as the Herald: one aimed fireball every 3 s (every 2 s in phase 2)
scoreboard players add @s ed_fb 1
execute if score @s ed_phase matches 1 if score @s ed_fb matches 60.. at @s anchored eyes facing entity @p[gamemode=!spectator] eyes run function {F}/shoot
execute if score @s ed_phase matches 2.. if score @s ed_fb matches 40.. at @s anchored eyes facing entity @p[gamemode=!spectator] eyes run function {F}/shoot
""")
    pack.function(f"{SS}/shoot", f"""
# as the Herald, at his eyes, facing the target. Direction = (point 1 block ahead) - (eye point).
scoreboard players set @s ed_fb 0
summon minecraft:fireball ^ ^ ^3 {fireball}
summon minecraft:marker ^ ^ ^ {{Tags:["ed_d0"]}}
summon minecraft:marker ^ ^ ^1 {{Tags:["ed_d1"]}}
execute store result score #x0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[0] 1000
execute store result score #y0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[1] 1000
execute store result score #z0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[2] 1000
execute store result score #x1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[0] 1000
execute store result score #y1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[1] 1000
execute store result score #z1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[2] 1000
scoreboard players operation #x1 ed_tmp -= #x0 ed_tmp
scoreboard players operation #y1 ed_tmp -= #y0 ed_tmp
scoreboard players operation #z1 ed_tmp -= #z0 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[0] double 0.0001 run scoreboard players get #x1 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[1] double 0.0001 run scoreboard players get #y1 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[2] double 0.0001 run scoreboard players get #z1 ed_tmp
kill @e[type=minecraft:marker,tag=ed_d0]
kill @e[type=minecraft:marker,tag=ed_d1]
tag @e[type=minecraft:fireball,tag=ed_fb_new] remove ed_fb_new
playsound minecraft:entity.ghast.shoot hostile @a[distance=..64] ~ ~ ~ 2 0.8
""")
    pack.function(f"{SS}/active", f"""
execute unless entity @a[distance=..64,gamemode=!spectator] run function {F}/reset
execute if entity @s[tag=ed_active] unless entity @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96] run function {F}/victory
execute if entity @s[tag=ed_active] run function {F}/active_boss
""")
    pack.function(f"{SS}/active_boss", f"""
bossbar set {BAR} players @a[distance=..64]
execute unless entity @e[type=minecraft:slime,tag=ed_herald_core,distance=..96] as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] at @s run function {F}/core_respawn
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] run function {F}/boss_tick
""")
    pack.function(f"{SS}/core_tick", f"""
# every tick, as the Storm Ruby (1000 HP so it can never die and split like a normal slime):
# damage it took this tick is dealt to the Herald x3, then it heals back to full.
execute store result score @s ed_hp run data get entity @s Health
scoreboard players set #d ed_tmp 1000
scoreboard players operation #d ed_tmp -= @s ed_hp
execute if score #d ed_tmp matches 1.. run function {F}/core_hit
data modify entity @s Health set value 1000f
""")
    pack.function(f"{SS}/core_hit", f"""
scoreboard players operation #d ed_tmp *= #3 ed_const
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] run function {F}/core_apply
execute at @s run particle minecraft:electric_spark ~ ~0.5 ~ 0.6 0.6 0.6 0.3 30
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @a[distance=..64] ~ ~ ~ 1.5 1.6
""")
    pack.function(f"{SS}/core_apply", f"""
# as the Herald: lower his health by #d (direct, so several hits in one moment all count)
execute store result score #b ed_tmp run data get entity @s Health
scoreboard players operation #b ed_tmp -= #d ed_tmp
execute if score #b ed_tmp matches ..0 run damage @s 9999 minecraft:generic_kill
execute if score #b ed_tmp matches 1.. store result entity @s Health float 1 run scoreboard players get #b ed_tmp
""")
    pack.function(f"{SS}/core_respawn", f"""
# as + at the Herald: the core was destroyed in one big hit; a new one forms above him
summon minecraft:slime ~ ~4.5 ~ {core_nbt % ""}
effect give @e[type=minecraft:slime,tag=ed_herald_core,distance=..8] minecraft:invisibility infinite 0 true
""")
    pack.function(f"{SS}/boss_tick", f"""
execute store result score @s ed_hp run data get entity @s Health
execute store result bossbar {BAR} value run scoreboard players get @s ed_hp
execute if score @s ed_phase matches 1 if score @s ed_hp matches ..200 run function {F}/phase2
scoreboard players add @s ed_wave 1
execute if score @s ed_wave matches 120.. run function {F}/riders
execute if score @s ed_phase matches 2 run scoreboard players add @s ed_timer 1
execute if score @s ed_phase matches 2 if score @s ed_timer matches 20.. run function {F}/lightning
""")
    pack.function(f"{SS}/riders", f"""
scoreboard players set @s ed_wave 0
execute if score @s ed_phase matches 2 run scoreboard players set @s ed_wave 20
summon minecraft:phantom ~12 ~8 ~12 {rider}
summon minecraft:phantom ~-12 ~8 ~-12 {rider}
summon minecraft:phantom ~12 ~8 ~-12 {rider}
execute if score @s ed_phase matches 2 run summon minecraft:phantom ~-12 ~8 ~12 {rider}
effect give @e[type=minecraft:phantom,tag=ed_herald_add,distance=..40] minecraft:fire_resistance infinite 0 true
playsound minecraft:entity.phantom.swoop hostile @a[distance=..64] ~ ~ ~ 2 0.7
""")
    pack.function(f"{SS}/phase2", f"""
scoreboard players set @s ed_phase 2
scoreboard players set @s ed_timer 0
tellraw @a[distance=..64] {{"text":"The storm breaks! Watch for sparks at your feet: lightning follows.","color":"aqua","bold":true}}
playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 2 0.8
""")
    pack.function(f"{SS}/lightning", f"""
# as the Herald, at the arena marker: mark a random player's spot; the strike lands 1 s later
scoreboard players set @s ed_timer 0
execute at @r[distance=..48,gamemode=!spectator] run summon minecraft:marker ~ ~ ~ {{Tags:["ed_strike"]}}
""")
    pack.function(f"{SS}/strike_tick", f"""
# every tick, as + at a lightning warning marker
particle minecraft:electric_spark ~ ~0.2 ~ 0.5 0.1 0.5 0.05 8
particle minecraft:end_rod ~ ~2 ~ 0.05 2 0.05 0 3
scoreboard players add @s ed_timer 1
execute if score @s ed_timer matches 20.. run summon minecraft:lightning_bolt ~ ~ ~
execute if score @s ed_timer matches 20.. run kill @s
""")
    pack.function(f"{SS}/victory", f"""
tag @s remove ed_active
tag @s add ed_done
bossbar set {BAR} visible false
execute if block ~ ~ ~ minecraft:chest unless data block ~ ~ ~ Items[0] run setblock ~ ~ ~ minecraft:air
execute unless block ~ ~ ~ minecraft:chest run setblock ~ ~ ~ minecraft:chest[facing=south]{{LootTable:"{ns}:chests/tempest_herald_reward"}}
execute if data block ~ ~ ~ Items[0] run loot spawn ~ ~1.5 ~ loot {ns}:chests/tempest_herald_reward
loot spawn ~ ~2 ~ loot {ns}:boss/tempest_herald
advancement grant @a[distance=..64] only {ns}:bosses/tempest_herald
title @a[distance=..64] title {{"text":"Herald Defeated","color":"gold","bold":true}}
title @a[distance=..64] subtitle {{"text":"the sky is quiet again","color":"yellow"}}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..64] ~ ~ ~ 1 1
kill @e[tag=ed_herald_add,distance=..64]
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..96] run data merge entity @s {{Size:0,DeathLootTable:"minecraft:empty"}}
kill @e[type=minecraft:slime,tag=ed_herald_core,distance=..96]
kill @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..96]
kill @e[type=minecraft:fireball,tag=ed_herald_fb,distance=..96]
kill @e[type=minecraft:marker,tag=ed_strike,distance=..96]
""")
    pack.function(f"{SS}/reset", f"""
tag @s remove ed_active
tag @s add ed_idle
bossbar set {BAR} visible false
execute as @e[tag=ed_herald_boss,distance=..96] run data merge entity @s {{DeathLootTable:"minecraft:empty"}}
execute as @e[tag=ed_herald_core,distance=..96] run data merge entity @s {{Size:0,DeathLootTable:"minecraft:empty"}}
execute as @e[tag=ed_herald_add,distance=..96] run data merge entity @s {{DeathLootTable:"minecraft:empty"}}
kill @e[tag=ed_herald_core,distance=..96]
kill @e[tag=ed_herald_boss,distance=..96]
kill @e[tag=ed_herald_add,distance=..96]
kill @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..96]
kill @e[type=minecraft:fireball,tag=ed_herald_fb,distance=..96]
kill @e[type=minecraft:marker,tag=ed_strike,distance=..96]
""")
    pack.function(f"{SS}/resupply", f"""
# as + at a resupply barrel marker: refill 4 stacks of rockets when a player is near and the barrel has none (60 s cooldown)
scoreboard players add @s ed_timer 0
scoreboard players remove @s[scores={{ed_timer=1..}}] ed_timer 1
execute if score @s ed_timer matches ..0 if entity @a[distance=..6] if block ~ ~ ~ minecraft:barrel unless data block ~ ~ ~ Items[{{id:"minecraft:firework_rocket"}}] run function {F}/refill
""")
    pack.function(f"{SS}/refill", f"""
data merge block ~ ~ ~ {{Items:[{{Slot:11b,id:"minecraft:firework_rocket",Count:64b}},{{Slot:12b,id:"minecraft:firework_rocket",Count:64b}},{{Slot:14b,id:"minecraft:firework_rocket",Count:64b}},{{Slot:15b,id:"minecraft:firework_rocket",Count:64b}}]}}
scoreboard players set @s ed_timer 240
particle minecraft:cloud ~ ~1 ~ 0.3 0.3 0.3 0.02 10
playsound minecraft:block.barrel.open block @a[distance=..8] ~ ~ ~ 1 1.2
""")

    tower = [
        pool([item_entry("firework_rocket", (16, 32))]),
        pool([item_entry("phantom_membrane", (1, 4), 6), item_entry("gold_ingot", (2, 6), 6),
              item_entry("diamond", (1, 2), 2), item_entry("ender_pearl", (1, 3), 3)], rolls=(2, 4)),
        pool([ammo_entry("308", (16, 32)), ammo_entry("338", (8, 15)), ammo_entry("556x45", (20, 40))], chance=0.6),
        pool([att_entry("scope_retro_2x"), att_entry("scope_contender"), att_entry("scope_acog_ta31"),
              att_entry("sniper_extended_mag_1")], chance=0.25),
    ]
    reward = [
        pool([item_entry("diamond", (4, 8))]), pool([item_entry("emerald", (6, 12))]),
        pool([item_entry("ghast_tear", (2, 4))]), pool([item_entry("netherite_scrap", 1)], chance=0.5),
        pool([item_entry("totem_of_undying", 1)], chance=0.2),
        pool([item_entry("book", None, 1, functions=[{"function": "minecraft:enchant_randomly"}])], rolls=2),
        pool([att_entry("scope_elcan_4x"), att_entry("scope_hamr"), att_entry("scope_standard_8x"),
              att_entry("sniper_extended_mag_2")], rolls=(1, 2)),
        pool([item_entry("firework_rocket", 64)]),
    ]
    write_loot(pack, ns, f"chests/{SS}_tower", tower)
    write_loot(pack, ns, "chests/tempest_herald_reward", reward)
    gunpool = boss_drop_tables(pack, ns, "tempest_herald", {"ai_awp": "338", "mk14": "308", "scar_h": "308"})
    write_loot(pack, ns, "boss/tempest_herald", [gunpool, pool([item_entry("ghast_tear", 3)]),
                                                  pool([item_entry("phantom_membrane", 4)])])
    advancement(pack, ns, "tempest_herald", "minecraft:ghast_tear", "Eye of the Storm",
                "Destroy the Tempest Herald above the Storm Spire")
    return {"bossbar": (BAR, "Tempest Herald", "blue", 400)}


# ============================================================================ THE HOLLOW

HO = "hollow"
DIM = "elytra_dungeons:the_hollow"
ARENA_ORIGIN = (-20, 80, -20)      # where the arena template is placed (it is 41 x 11 x 41)
ARRIVE = "0.5 85 12.5 180 0"       # arrival point: south part of the arena, facing the altar


def gate_template():
    """Rift Gate, 11 x 9 x 7: a ruined crying-obsidian frame. Step into it to enter the Hollow."""
    rnd = random.Random(5)
    t = Template(11, 9, 7)
    t.fill(0, 1, 0, 10, 8, 6, "air")
    for x in range(11):
        for z in range(7):
            t.set(x, 0, z, rnd.choice(["blackstone", "polished_blackstone", "cobbled_deepslate", "obsidian"]))
    t.fill(3, 1, 3, 3, 6, 3, "crying_obsidian")
    t.fill(7, 1, 3, 7, 6, 3, "crying_obsidian")
    t.fill(3, 6, 3, 7, 6, 3, "crying_obsidian")
    t.set(5, 6, 3, "obsidian")
    for (x, z, h) in ((0, 0, 3), (10, 0, 1), (0, 6, 2), (10, 6, 4)):
        t.fill(x, 1, z, x, h, z, "obsidian")
    t.set(10, 5, 6, "end_rod[facing=up]")
    t.set(1, 1, 5, "amethyst_cluster[facing=up,waterlogged=false]")
    t.set(9, 1, 1, "amethyst_cluster[facing=up,waterlogged=false]")
    t.entity(5, 1, 3, {"id": "minecraft:marker", "Tags": ["ed_rift_in"]})
    return t


def arena_template():
    """41 x 11 x 41 floating obsidian arena, placed once at ARENA_ORIGIN in the Hollow.
    Built from blast-resistant blocks around the pillars because end crystals explode."""
    rnd = random.Random(7)
    t = Template(41, 11, 41)
    c = 20
    for y in range(0, 4):                                               # rough underside
        r = 9 + y * 3
        for x in range(41):
            for z in range(41):
                d = math.hypot(x - c, z - c)
                if d <= r and not (d > r - 1.5 and rnd.random() < 0.4):
                    t.set(x, y, z, rnd.choice(["obsidian", "obsidian", "blackstone", "crying_obsidian"]))
    for x in range(41):                                                 # floor with crying-obsidian rings
        for z in range(41):
            d = math.hypot(x - c, z - c)
            if d <= 19.4:
                b = "crying_obsidian" if (15 <= d < 16.2 or 6.5 <= d < 7.5) else "obsidian"
                t.set(x, 4, z, b)
    t.set(20, 4, 32, "obsidian")                                        # arrival floor (checked by the build step)
    t.fill(18, 5, 18, 22, 5, 22, "crying_obsidian")                     # altar
    t.set(20, 5, 20, "obsidian")
    for px, pz in ((10, 10), (30, 10), (10, 30), (30, 30)):             # crystal pillars (diagonals)
        t.fill(px - 1, 5, pz - 1, px + 1, 10, pz + 1, "obsidian")
        t.set(px, 10, pz, "crying_obsidian")
    for dx, dz in ((18, 0), (-18, 0), (0, -18), (11, 0), (-11, 0), (0, -11)):  # lights on the axes
        t.set(c + dx, 4, c + dz, "pearlescent_froglight[axis=y]")
    for dx, dz in ((18, 0), (-18, 0), (0, -18)):
        t.set(c + dx, 5, c + dz, "end_rod[facing=up]")
    t.fill(18, 5, 37, 18, 10, 37, "crying_obsidian")                    # return rift frame (south)
    t.fill(22, 5, 37, 22, 10, 37, "crying_obsidian")
    t.fill(18, 10, 37, 22, 10, 37, "crying_obsidian")
    t.entity(20, 5, 37, {"id": "minecraft:marker", "Tags": ["ed_rift_out"]})
    t.entity(20, 6, 20, {"id": "minecraft:marker", "Tags": ["ed_arena", "ed_hollow", "ed_idle"]})
    return t


def hollow(pack, ns, template_pool):
    # ---- dimension
    pack.json(f"data/{ns}/dimension_type/the_hollow.json", {
        "ambient_light": 0.05, "bed_works": False, "coordinate_scale": 1.0, "effects": "minecraft:the_end",
        "fixed_time": 18000, "has_ceiling": False, "has_raids": False, "has_skylight": False, "height": 256,
        "infiniburn": "#minecraft:infiniburn_end", "logical_height": 256, "min_y": 0,
        "monster_spawn_block_light_limit": 0, "monster_spawn_light_level": 0, "natural": False,
        "piglin_safe": False, "respawn_anchor_works": False, "ultrawarm": False})
    pack.json(f"data/{ns}/worldgen/biome/hollow.json", {
        "carvers": {}, "downfall": 0.0,
        "effects": {"fog_color": 1704737, "sky_color": 0, "water_color": 4159204, "water_fog_color": 329011,
                    "mood_sound": {"block_search_extent": 8, "offset": 2.0, "sound": "minecraft:ambient.cave",
                                   "tick_delay": 6000}},
        "features": [[] for _ in range(11)], "has_precipitation": False, "spawn_costs": {},
        "spawners": {k: [] for k in ("ambient", "axolotls", "creature", "misc", "monster",
                                     "underground_water_creature", "water_ambient", "water_creature")},
        "temperature": 0.5})
    pack.json(f"data/{ns}/dimension/the_hollow.json", {
        "type": f"{ns}:the_hollow",
        "generator": {"type": "minecraft:flat", "settings": {
            "biome": f"{ns}:hollow", "features": False, "lakes": False,
            "layers": [{"block": "minecraft:air", "height": 1}], "structure_overrides": []}}})

    # ---- rift gate structure (overworld)
    pack.template(f"{HO}/gate", gate_template())
    pack.template(f"{HO}/arena", arena_template())
    template_pool(pack, f"{HO}/gate", [(f"{HO}/gate", 1)], "minecraft:empty")
    pack.json(f"data/{ns}/tags/worldgen/biome/has_structure/rift_gate.json", {"values": [
        "#minecraft:is_forest", "#minecraft:is_taiga", "#minecraft:is_jungle", "#minecraft:is_savanna",
        "#minecraft:is_badlands", "minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow",
        "minecraft:desert", "minecraft:swamp", "minecraft:snowy_plains", "minecraft:dark_forest"]})
    pack.json(f"data/{ns}/worldgen/structure/rift_gate.json", {
        "type": "minecraft:jigsaw", "biomes": f"#{ns}:has_structure/rift_gate", "max_distance_from_center": 80,
        "project_start_to_heightmap": "WORLD_SURFACE_WG", "size": 1, "spawn_overrides": {},
        "start_height": {"absolute": 0}, "start_pool": f"{ns}:{HO}/gate", "step": "surface_structures",
        "terrain_adaptation": "beard_thin", "use_expansion_hack": False})
    pack.json(f"data/{ns}/worldgen/structure_set/rift_gate.json", {
        "placement": {"type": "minecraft:random_spread", "salt": 903117455, "separation": 24, "spacing": 64},
        "structures": [{"structure": f"{ns}:rift_gate", "weight": 1}]})

    F = f"{ns}:{HO}"
    BAR = f"{ns}:hollow_magus"
    ox, oy, oz = ARENA_ORIGIN
    magus = ('{Tags:["ed_magus_boss","ed_boss","ed_shield_up"],'
             'CustomName:\'{"text":"Hollow Magus","color":"light_purple","bold":true}\',CustomNameVisible:1b,'
             'PersistenceRequired:1b,Health:500f,Attributes:[{Name:"minecraft:generic.max_health",Base:500d},'
             '{Name:"minecraft:generic.armor",Base:6d},{Name:"minecraft:generic.follow_range",Base:48d},'
             '{Name:"minecraft:generic.knockback_resistance",Base:0.6d}],'
             'HandItems:[{id:"minecraft:bow",Count:1b,tag:{Enchantments:[{id:"minecraft:power",lvl:2s}]}},{}],'
             'HandDropChances:[0f,0f]}')
    crystal = '{Tags:["ed_magus_crystal"],ShowBottom:0b,BeamTarget:{X:0,Y:88,Z:0}}'
    vex = '{Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}'

    # ---- travel
    pack.function(f"{HO}/rift_in", f"""
# as + at a Rift Gate marker (overworld)
execute if entity @a[distance=..24] run particle minecraft:portal ~ ~1.8 ~ 0.6 1.2 0.2 0.6 25
execute if entity @a[distance=..24] run particle minecraft:reverse_portal ~ ~1.8 ~ 0.5 1.0 0.1 0.02 6
execute as @a[distance=..1.6,gamemode=!spectator,scores={{ed_cd=..0}}] run function {F}/enter
""")
    pack.function(f"{HO}/enter", f"""
# as the player, positioned at the gate: remember where to send them back (3 blocks out of the frame)
function {F}/clear_return
execute positioned ~ ~ ~3 run summon minecraft:marker ~ ~ ~ {{Tags:["ed_return","ed_new"]}}
scoreboard players operation @e[type=minecraft:marker,tag=ed_new,limit=1] ed_pid = @s ed_pid
execute as @e[type=minecraft:marker,tag=ed_new] at @s run forceload add ~ ~
tag @e[type=minecraft:marker,tag=ed_new] remove ed_new
scoreboard players set @s ed_cd 20
effect give @s minecraft:nausea 4 0 true
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.2
tag @s add ed_to_hollow
execute if score #built ed_flag matches 1 run function {F}/deliver
execute unless score #built ed_flag matches 1 run function {F}/build
""")
    pack.function(f"{HO}/build", f"""
# first visit in this world: load the arena area and place the arena
execute in {DIM} run forceload add -32 -32 31 31
tellraw @a[tag=ed_to_hollow] {{"text":"The rift tears open...","color":"light_purple","italic":true}}
schedule function {F}/place 10t replace
""")
    pack.function(f"{HO}/place", f"""
execute in {DIM} run place template {ns}:{HO}/arena {ox} {oy} {oz}
execute in {DIM} if block 0 84 12 minecraft:obsidian run scoreboard players set #built ed_flag 1
execute if score #built ed_flag matches 1 run schedule function {F}/deliver 2t replace
execute unless score #built ed_flag matches 1 run schedule function {F}/place 10t replace
""")
    pack.function(f"{HO}/deliver", f"""
execute as @a[tag=ed_to_hollow] in {DIM} run tp @s {ARRIVE}
effect give @a[tag=ed_to_hollow] minecraft:slow_falling 5 0 true
tag @a[tag=ed_to_hollow] remove ed_to_hollow
""")
    pack.function(f"{HO}/rift_out", f"""
# as + at the return rift in the Hollow
execute if entity @a[distance=..24] run particle minecraft:portal ~ ~1.8 ~ 0.6 1.2 0.2 0.6 25
execute as @a[distance=..1.6,gamemode=!spectator,scores={{ed_cd=..0}}] run function {F}/leave
""")
    pack.function(f"{HO}/leave", f"""
tag @s add ed_returning
scoreboard players operation #cur ed_pid = @s ed_pid
scoreboard players set #found ed_tmp 0
execute as @e[type=minecraft:marker,tag=ed_return] if score @s ed_pid = #cur ed_pid at @s run function {F}/return_here
execute if score #found ed_tmp matches 0 in minecraft:overworld run spreadplayers 0 0 0 8 false @s
effect give @s minecraft:slow_falling 5 0 true
scoreboard players set @s ed_cd 20
tag @s remove ed_returning
""")
    pack.function(f"{HO}/return_here", f"""
# as + at this player's return marker in the overworld
tp @a[tag=ed_returning,limit=1] ~ ~ ~
forceload remove ~ ~
scoreboard players set #found ed_tmp 1
kill @s
""")
    pack.function(f"{HO}/clear_return", f"""
scoreboard players operation #cur ed_pid = @s ed_pid
execute as @e[type=minecraft:marker,tag=ed_return] if score @s ed_pid = #cur ed_pid at @s run function {F}/drop_return
""")
    pack.function(f"{HO}/drop_return", """
forceload remove ~ ~
kill @s
""")
    pack.function(f"{HO}/on_death", f"""
function {F}/clear_return
scoreboard players set @s ed_deaths 0
""")
    pack.function(f"{HO}/void_net", f"""
# as a player in the Hollow who fell below y=70: back to the arrival point, a little hurt
tp @s {ARRIVE}
effect give @s minecraft:slow_falling 4 0 true
damage @s 4 minecraft:generic
tellraw @s {{"text":"The Hollow spits you back out.","color":"dark_purple","italic":true}}
""")

    # ---- fight
    pack.function(f"{HO}/arena_tick", f"""
execute if entity @s[tag=ed_idle] if entity @a[distance=..9,gamemode=!spectator] run function {F}/start
execute if entity @s[tag=ed_active] run function {F}/active
execute if entity @s[tag=ed_done] run function {F}/done_tick
""")
    pack.function(f"{HO}/start", f"""
tag @s remove ed_idle
tag @s add ed_active
execute if block ~ ~ ~ minecraft:chest run setblock ~ ~ ~ minecraft:air destroy
summon minecraft:illusioner ~ ~ ~ {magus}
function {F}/scale_boss
scoreboard players set @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] ed_phase 1
scoreboard players set @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] ed_wave 0
effect give @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] minecraft:resistance infinite 4 true
function {F}/crystals
bossbar set {BAR} players @a[distance=..64]
bossbar set {BAR} value 500
bossbar set {BAR} visible true
title @a[distance=..64] title {{"text":"The Hollow Magus","color":"light_purple","bold":true}}
title @a[distance=..64] subtitle {{"text":"shoot the crystals to break his shield","color":"gray"}}
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 1 0.8
""")
    pack.function(f"{HO}/crystals", f"""
# four end crystals on the pillars (positions are relative to the altar marker)
summon minecraft:end_crystal ~-10 ~5 ~-10 {crystal}
summon minecraft:end_crystal ~10 ~5 ~-10 {crystal}
summon minecraft:end_crystal ~-10 ~5 ~10 {crystal}
summon minecraft:end_crystal ~10 ~5 ~10 {crystal}
playsound minecraft:block.beacon.activate hostile @a[distance=..64] ~ ~ ~ 2 0.8
""")
    pack.function(f"{HO}/active", f"""
execute unless entity @a[distance=..64,gamemode=!spectator] run function {F}/reset
execute if entity @s[tag=ed_active] unless entity @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..64] run function {F}/victory
execute if entity @s[tag=ed_active] run function {F}/active_boss
""")
    pack.function(f"{HO}/active_boss", f"""
execute as @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=16..64] run tp @s ~ ~ ~
bossbar set {BAR} players @a[distance=..64]
execute as @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..64,limit=1] run function {F}/boss_tick
""")
    pack.function(f"{HO}/boss_tick", f"""
# as the Magus, positioned at the altar marker
execute store result score @s ed_hp run data get entity @s Health
execute store result bossbar {BAR} value run scoreboard players get @s ed_hp
execute store result score #crystals ed_tmp if entity @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..32]
execute if entity @s[tag=ed_shield_up] if score #crystals ed_tmp matches 0 run function {F}/shield_down
execute if entity @s[tag=!ed_shield_up] run function {F}/shield_timer
execute if score @s ed_phase matches 1 if score @s ed_hp matches ..330 run function {F}/phase2
execute if score @s ed_phase matches 2 if score @s ed_hp matches ..160 run function {F}/phase3
scoreboard players add @s ed_wave 1
execute if score @s ed_wave matches 80.. run function {F}/wave
execute if score @s ed_phase matches 3 run scoreboard players add @s ed_timer 1
execute if score @s ed_phase matches 3 if score @s ed_timer matches 24.. at @s run function {F}/pulse
scoreboard players add @s ed_fb 1
execute if score @s ed_fb matches 16.. at @s facing entity @p[gamemode=!spectator] feet rotated ~ 0 positioned ~ 85 ~ run function {F}/fangs
""")
    pack.function(f"{HO}/fangs", """
# a line of evoker fangs racing toward the nearest player (arena floor surface is y=85)
scoreboard players set @s ed_fb 0
summon minecraft:evoker_fangs ^ ^ ^2 {Warmup:0}
summon minecraft:evoker_fangs ^ ^ ^3.5 {Warmup:2}
summon minecraft:evoker_fangs ^ ^ ^5 {Warmup:4}
summon minecraft:evoker_fangs ^ ^ ^6.5 {Warmup:6}
summon minecraft:evoker_fangs ^ ^ ^8 {Warmup:8}
summon minecraft:evoker_fangs ^ ^ ^9.5 {Warmup:10}
summon minecraft:evoker_fangs ^ ^ ^11 {Warmup:12}
summon minecraft:evoker_fangs ^ ^ ^12.5 {Warmup:14}
summon minecraft:evoker_fangs ^ ^ ^14 {Warmup:16}
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..48] ~ ~ ~ 1.5 0.8
""")
    pack.function(f"{HO}/scale_boss", """
# needs the Pehkui mod: the Magus is twice player size; motion 0.6 keeps his walking speed close to normal
scale set pehkui:base 2 @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8]
scale set pehkui:motion 0.6 @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8]
""")
    pack.function(f"{HO}/shield_down", f"""
tag @s remove ed_shield_up
effect clear @s minecraft:resistance
effect give @s minecraft:glowing infinite 0 true
scoreboard players set @s ed_shield 0
title @a[distance=..64] actionbar {{"text":"SHIELD BROKEN - shoot him now!","color":"light_purple","bold":true}}
playsound minecraft:block.beacon.deactivate hostile @a[distance=..64] ~ ~ ~ 2 0.7
function {F}/ammo_drop
""")
    pack.function(f"{HO}/shield_timer", f"""
# shield comes back after 15 seconds (60 loops of 5 ticks), with fresh crystals
scoreboard players add @s ed_shield 1
execute if score @s ed_shield matches 60.. run function {F}/shield_up
""")
    pack.function(f"{HO}/shield_up", f"""
tag @s add ed_shield_up
effect give @s minecraft:resistance infinite 4 true
effect clear @s minecraft:glowing
function {F}/crystals
title @a[distance=..64] actionbar {{"text":"The Magus raises his shield. Break the crystals!","color":"dark_purple"}}
""")
    pack.function(f"{HO}/ammo_drop", """
summon minecraft:item ~ ~1 ~ {Item:{id:"tacz:ammo",Count:30b,tag:{AmmoId:"tacz:556x45"}},PickupDelay:10s}
summon minecraft:item ~ ~1 ~ {Item:{id:"tacz:ammo",Count:24b,tag:{AmmoId:"tacz:308"}},PickupDelay:10s}
summon minecraft:item ~ ~1 ~ {Item:{id:"tacz:ammo",Count:18b,tag:{AmmoId:"tacz:12g"}},PickupDelay:10s}
summon minecraft:item ~ ~1 ~ {Item:{id:"tacz:ammo",Count:30b,tag:{AmmoId:"tacz:9mm"}},PickupDelay:10s}
particle minecraft:end_rod ~ ~1.5 ~ 0.5 0.5 0.5 0.1 40
""")
    pack.function(f"{HO}/phase2", f"""
scoreboard players set @s ed_phase 2
effect give @s minecraft:speed infinite 0 true
tellraw @a[distance=..64] {{"text":"The Magus calls the Hollow's wisps!","color":"light_purple"}}
function {F}/wave
""")
    pack.function(f"{HO}/phase3", f"""
scoreboard players set @s ed_phase 3
scoreboard players set @s ed_timer 0
tellraw @a[distance=..64] {{"text":"The void itself rejects you. Keep your wings ready!","color":"dark_purple","bold":true}}
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..64] ~ ~ ~ 2 0.5
""")
    pack.function(f"{HO}/wave", f"""
scoreboard players set @s ed_wave 0
summon minecraft:vex ~-6 ~4 ~ {vex}
summon minecraft:vex ~6 ~4 ~ {vex}
summon minecraft:vex ~ ~4 ~-6 {vex}
execute if score @s ed_phase matches 2.. run summon minecraft:vex ~ ~4 ~6 {vex}
execute if score @s ed_phase matches 3 run summon minecraft:vex ~ ~6 ~ {vex}
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..64] ~ ~ ~ 2 0.8
""")
    pack.function(f"{HO}/pulse", f"""
# as + at the Magus: everyone within 7 blocks is thrown upward
scoreboard players set @s ed_timer 0
particle minecraft:reverse_portal ~ ~1 ~ 3 1 3 0.1 200
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 1 1.4
effect give @a[distance=..7,gamemode=!creative,gamemode=!spectator] minecraft:levitation 1 3 true
""")
    pack.function(f"{HO}/victory", f"""
tag @s remove ed_active
tag @s add ed_done
scoreboard players set @s ed_timer 0
bossbar set {BAR} visible false
execute if block ~ ~ ~2 minecraft:chest unless data block ~ ~ ~2 Items[0] run setblock ~ ~ ~2 minecraft:air
execute unless block ~ ~ ~2 minecraft:chest run setblock ~ ~ ~2 minecraft:chest[facing=south]{{LootTable:"{ns}:chests/hollow_magus_reward"}}
execute if data block ~ ~ ~2 Items[0] run loot spawn ~ ~1.5 ~2 loot {ns}:chests/hollow_magus_reward
loot spawn ~ ~2 ~ loot {ns}:boss/hollow_magus
advancement grant @a[distance=..64] only {ns}:bosses/hollow_magus
title @a[distance=..64] title {{"text":"Magus Defeated","color":"gold","bold":true}}
title @a[distance=..64] subtitle {{"text":"the rift to the south leads home","color":"yellow"}}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..64] ~ ~ ~ 1 1
kill @e[tag=ed_magus_add,distance=..64]
tp @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..64] ~ -300 ~
""")
    pack.function(f"{HO}/reset", f"""
tag @s remove ed_active
tag @s add ed_idle
bossbar set {BAR} visible false
execute as @e[tag=ed_magus_boss,distance=..64] run data merge entity @s {{DeathLootTable:"minecraft:empty"}}
execute as @e[tag=ed_magus_add,distance=..64] run data merge entity @s {{DeathLootTable:"minecraft:empty"}}
kill @e[tag=ed_magus_boss,distance=..64]
kill @e[tag=ed_magus_add,distance=..64]
tp @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..64] ~ -300 ~
""")
    pack.function(f"{HO}/done_tick", f"""
# after a win the Magus returns once nobody has been here for 10 minutes (2400 loops of 5 ticks)
execute if entity @a[distance=..80] run scoreboard players set @s ed_timer 0
execute unless entity @a[distance=..80] run scoreboard players add @s ed_timer 1
execute if score @s ed_timer matches 2400.. run function {F}/rearm
""")
    pack.function(f"{HO}/rearm", """
tag @s remove ed_done
tag @s add ed_idle
scoreboard players set @s ed_timer 0
""")

    reward = [
        pool([item_entry("diamond", (6, 10))]), pool([item_entry("emerald", (8, 16))]),
        pool([item_entry("netherite_ingot", 1)], chance=0.4), pool([item_entry("echo_shard", (2, 4))]),
        pool([item_entry("totem_of_undying", 1)], chance=0.5),
        pool([item_entry("book", None, 1, functions=[{"function": "minecraft:enchant_randomly"}])], rolls=2),
        pool([att_entry("ammo_mod_hp"), att_entry("ammo_mod_fmj"), att_entry("extended_mag_2"),
              att_entry("muzzle_silencer_ursus"), att_entry("scope_mk5hd")], rolls=(1, 2)),
        pool([ammo_entry("556x45", 60), ammo_entry("12g", 36), ammo_entry("45acp", 60)]),
    ]
    write_loot(pack, ns, "chests/hollow_magus_reward", reward)
    gunpool = boss_drop_tables(pack, ns, "hollow_magus",
                               {"m249": "556x45", "spas_12": "12g", "vector45": "45acp", "aa12": "12g"})
    write_loot(pack, ns, "boss/hollow_magus", [gunpool, pool([item_entry("ender_pearl", 4)])])
    advancement(pack, ns, "hollow_magus", "minecraft:end_crystal", "Into the Hollow",
                "Break the Hollow Magus's shield and defeat him")
    return {"bossbar": (BAR, "Hollow Magus", "purple", 500)}
