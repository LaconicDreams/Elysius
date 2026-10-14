# As the spot marker, at the candidate surface spot. Sets #good mh_tmp to 0 when the spot is bad.
# natural ground below (no water, leaves, planks, bricks...), two free blocks for the zombie
execute unless block ~ ~-1 ~ #elytra_hordes:horde_ground run scoreboard players set #good mh_tmp 0
execute unless block ~ ~ ~ #elytra_hordes:horde_air run scoreboard players set #good mh_tmp 0
execute unless block ~ ~1 ~ #elytra_hordes:horde_air run scoreboard players set #good mh_tmp 0
# not inside villages, outposts, temples, dungeon structures (list in predicates/horde/in_structure.json)
execute if score #good mh_tmp matches 1 if predicate modpack:horde/in_structure run scoreboard players set #good mh_tmp 0
# not within 100 blocks of world spawn, not within 96 blocks of a boss arena or rift gate
execute if entity @e[type=minecraft:marker,tag=mh_spawn,distance=..100] run scoreboard players set #good mh_tmp 0
execute if entity @e[type=minecraft:marker,tag=ed_arena,distance=..96] run scoreboard players set #good mh_tmp 0
execute if entity @e[type=minecraft:marker,tag=ed_rift_in,distance=..96] run scoreboard players set #good mh_tmp 0
