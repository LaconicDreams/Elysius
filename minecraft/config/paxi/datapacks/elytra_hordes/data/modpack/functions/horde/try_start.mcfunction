# As the player, at the player, after a successful roll: safety checks, then begin.
scoreboard players set #ok mh_tmp 1
# not underground: the player must be at most 8 blocks below the surface above them
execute positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["mh_probe"]}
execute store result score #sy mh_tmp run data get entity @e[type=minecraft:marker,tag=mh_probe,limit=1] Pos[1]
kill @e[type=minecraft:marker,tag=mh_probe]
scoreboard players remove #sy mh_tmp 8
execute store result score #y mh_tmp run data get entity @s Pos[1]
execute if score #y mh_tmp < #sy mh_tmp run scoreboard players set #ok mh_tmp 0
# never during another horde
execute if entity @e[type=#elytra_hordes:horde_types,tag=modpack_horde,distance=..160] run scoreboard players set #ok mh_tmp 0
# not near boss arenas or rift gates
execute if entity @e[type=minecraft:marker,tag=ed_arena,distance=..128] run scoreboard players set #ok mh_tmp 0
execute if entity @e[type=minecraft:marker,tag=ed_rift_in,distance=..128] run scoreboard players set #ok mh_tmp 0
# caps
execute store result score #n mh_tmp if entity @e[type=#elytra_hordes:hostiles,distance=..64]
execute if score #n mh_tmp >= #max_hostiles mh_cfg run scoreboard players set #ok mh_tmp 0
execute store result score #n mh_tmp if entity @e[type=#elytra_hordes:horde_types,tag=modpack_horde]
execute if score #n mh_tmp >= #max_horde_total mh_cfg run scoreboard players set #ok mh_tmp 0
execute if score #ok mh_tmp matches 1 run function modpack:horde/begin
