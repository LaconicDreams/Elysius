# At the spot. Spawns one horde zombie, then repeats until #i reaches #size.
# NBT is given, so the game does not randomise them (no babies, no chicken jockeys, no
# reinforcement calls, no random gear); persistent until this pack removes them (member_tick).
function modpack:horde/random
scoreboard players operation #r mh_tmp %= #100 mh_const
execute if score #kind mh_tmp matches 0 if score #r mh_tmp matches 0..84 run summon minecraft:zombie ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute if score #kind mh_tmp matches 0 if score #r mh_tmp matches 85..99 run summon minecraft:zombie_villager ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute if score #kind mh_tmp matches 1 if score #r mh_tmp matches 0..69 run summon minecraft:husk ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute if score #kind mh_tmp matches 1 if score #r mh_tmp matches 70..99 run summon minecraft:zombie ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute if score #kind mh_tmp matches 2 if score #r mh_tmp matches 0..39 run summon minecraft:drowned ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute if score #kind mh_tmp matches 2 if score #r mh_tmp matches 40..99 run summon minecraft:zombie ~ ~ ~ {Tags:["modpack_horde","mh_new"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48.0d}]}
execute as @e[type=#elytra_hordes:horde_types,tag=mh_new,distance=..1,limit=1] run function modpack:horde/equip
scoreboard players add #i mh_tmp 1
execute if score #i mh_tmp < #size mh_tmp run function modpack:horde/spawn_member
