tag @s remove ed_idle
tag @s add ed_active
scoreboard players set @s ed_angle 0
summon minecraft:ghast ~ ~11 ~10 {Tags:["ed_herald_boss","ed_boss"],CustomName:'{"text":"Tempest Herald","color":"aqua","bold":true}',CustomNameVisible:1b,PersistenceRequired:1b,NoAI:1b,Health:400f,Attributes:[{Name:"minecraft:generic.max_health",Base:400d}]}
summon minecraft:slime ~ ~15.5 ~10 {Size:1,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,Health:1000f,Attributes:[{Name:"minecraft:generic.max_health",Base:1000d}],Tags:["ed_herald_core"],CustomName:'{"text":"Storm Ruby","color":"red","bold":true}'}
summon minecraft:item_display ~ ~13 ~10 {Tags:["ed_herald_vis"],item:{id:"minecraft:paper",Count:1b,tag:{CustomModelData:7101}},item_display:"none",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[4f,4f,4f]},view_range:2f}
effect give @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] minecraft:resistance infinite 3 true
effect give @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] minecraft:invisibility infinite 0 true
effect give @e[type=minecraft:slime,tag=ed_herald_core,distance=..24] minecraft:invisibility infinite 0 true
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_phase 1
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_wave 100
scoreboard players set @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..24] ed_fb 0
bossbar set elytra_dungeons:tempest_herald players @a[distance=..64]
bossbar set elytra_dungeons:tempest_herald value 400
bossbar set elytra_dungeons:tempest_herald visible true
title @a[distance=..64] title {"text":"The Tempest Herald","color":"aqua","bold":true}
title @a[distance=..64] subtitle {"text":"shoot the ruby on his forehead","color":"gray"}
playsound minecraft:entity.ghast.scream hostile @a[distance=..64] ~ ~ ~ 2 0.5
