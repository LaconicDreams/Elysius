# As the target player, at the player: work out the size, find a spot, spawn, warn.
kill @e[type=minecraft:marker,tag=mh_spot]
# size = #size_min + random(0..#size_rand) + #mp_bonus * min(extra players within 64, #mp_max_players), capped
function modpack:horde/random
scoreboard players operation #size mh_tmp = #r mh_tmp
scoreboard players operation #span mh_tmp = #size_rand mh_cfg
scoreboard players add #span mh_tmp 1
scoreboard players operation #size mh_tmp %= #span mh_tmp
scoreboard players operation #size mh_tmp += #size_min mh_cfg
execute store result score #pl mh_tmp if entity @a[gamemode=!spectator,distance=..64]
scoreboard players remove #pl mh_tmp 1
execute if score #pl mh_tmp > #mp_max_players mh_cfg run scoreboard players operation #pl mh_tmp = #mp_max_players mh_cfg
scoreboard players operation #pl mh_tmp *= #mp_bonus mh_cfg
scoreboard players operation #size mh_tmp += #pl mh_tmp
execute if score #size mh_tmp > #size_cap mh_cfg run scoreboard players operation #size mh_tmp = #size_cap mh_cfg
# up to 12 tries to find a spot
scoreboard players set #tries mh_tmp 12
scoreboard players set #found mh_tmp 0
function modpack:horde/find_spot
execute if score #found mh_tmp matches 1 as @e[type=minecraft:marker,tag=mh_spot,distance=..120,limit=1] at @s run function modpack:horde/spawn_horde
execute if score #found mh_tmp matches 1 run function modpack:horde/announce
execute if score #found mh_tmp matches 0 run tellraw @s[tag=mh_force] {"text":"[Hordes] No valid spot 40-70 blocks around you (water, structure, world spawn or boss arena nearby, or unloaded chunks). Try again elsewhere.","color":"red"}
kill @e[type=minecraft:marker,tag=mh_spot]
