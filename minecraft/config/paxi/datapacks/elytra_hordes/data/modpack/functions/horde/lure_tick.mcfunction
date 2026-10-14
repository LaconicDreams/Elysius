# Every 5 s, as a player with a running lure, at the player. Renews the lure sense every 10 s while
# the player is at or below #max_y and a horde zombie is within 128 blocks.
scoreboard players remove @s mh_lure 5
scoreboard players operation #m mh_tmp = @s mh_lure
scoreboard players operation #m mh_tmp %= #10 mh_const
execute store result score #y mh_tmp run data get entity @s Pos[1]
execute if score #m mh_tmp matches 0 if score #y mh_tmp <= #max_y mh_cfg if entity @e[type=#elytra_hordes:horde_types,tag=modpack_horde,distance=..128] run function modpack:noise/lure
