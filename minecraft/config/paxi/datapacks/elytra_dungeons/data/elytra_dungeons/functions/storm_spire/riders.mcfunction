scoreboard players set @s ed_wave 0
execute if score @s ed_phase matches 2 run scoreboard players set @s ed_wave 20
summon minecraft:phantom ~12 ~8 ~12 {Tags:["ed_add","ed_herald_add"],PersistenceRequired:1b,CustomName:'{"text":"Storm Rider","color":"gray"}'}
summon minecraft:phantom ~-12 ~8 ~-12 {Tags:["ed_add","ed_herald_add"],PersistenceRequired:1b,CustomName:'{"text":"Storm Rider","color":"gray"}'}
summon minecraft:phantom ~12 ~8 ~-12 {Tags:["ed_add","ed_herald_add"],PersistenceRequired:1b,CustomName:'{"text":"Storm Rider","color":"gray"}'}
execute if score @s ed_phase matches 2 run summon minecraft:phantom ~-12 ~8 ~12 {Tags:["ed_add","ed_herald_add"],PersistenceRequired:1b,CustomName:'{"text":"Storm Rider","color":"gray"}'}
effect give @e[type=minecraft:phantom,tag=ed_herald_add,distance=..40] minecraft:fire_resistance infinite 0 true
playsound minecraft:entity.phantom.swoop hostile @a[distance=..64] ~ ~ ~ 2 0.7
