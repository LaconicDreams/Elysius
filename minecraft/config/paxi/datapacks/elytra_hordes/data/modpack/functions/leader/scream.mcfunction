scoreboard players set @s ld_t 0
scoreboard players add @s ld_sum 2
playsound minecraft:entity.ghast.scream hostile @a[distance=..64] ~ ~ ~ 3 0.6
particle minecraft:angry_villager ~ ~2 ~ 0.6 0.4 0.6 0 8
title @a[distance=..32] actionbar {"text":"The Schreier screams for the horde!","color":"light_purple"}
summon minecraft:zombie ~2 ~ ~0 {Tags:["modpack_horde","ld_called"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48d}]}
summon minecraft:zombie ~-2 ~ ~0 {Tags:["modpack_horde","ld_called"],PersistenceRequired:1b,Attributes:[{Name:"minecraft:generic.follow_range",Base:48d}]}
