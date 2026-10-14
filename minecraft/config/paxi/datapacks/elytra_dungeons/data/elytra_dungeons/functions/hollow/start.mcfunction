tag @s remove ed_idle
tag @s add ed_active
execute if block ~ ~ ~ minecraft:chest run setblock ~ ~ ~ minecraft:air destroy
summon minecraft:illusioner ~ ~ ~ {Tags:["ed_magus_boss","ed_boss","ed_shield_up"],CustomName:'{"text":"Hollow Magus","color":"light_purple","bold":true}',CustomNameVisible:1b,PersistenceRequired:1b,Health:500f,Attributes:[{Name:"minecraft:generic.max_health",Base:500d},{Name:"minecraft:generic.armor",Base:6d},{Name:"minecraft:generic.follow_range",Base:48d},{Name:"minecraft:generic.knockback_resistance",Base:0.6d}],HandItems:[{id:"minecraft:bow",Count:1b,tag:{Enchantments:[{id:"minecraft:power",lvl:2s}]}},{}],HandDropChances:[0f,0f]}
function elytra_dungeons:hollow/scale_boss
scoreboard players set @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] ed_phase 1
scoreboard players set @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] ed_wave 0
effect give @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..8] minecraft:resistance infinite 4 true
function elytra_dungeons:hollow/crystals
bossbar set elytra_dungeons:hollow_magus players @a[distance=..64]
bossbar set elytra_dungeons:hollow_magus value 500
bossbar set elytra_dungeons:hollow_magus visible true
title @a[distance=..64] title {"text":"The Hollow Magus","color":"light_purple","bold":true}
title @a[distance=..64] subtitle {"text":"shoot the crystals to break his shield","color":"gray"}
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 1 0.8
