tag @s remove ed_idle
tag @s add ed_active
summon minecraft:wither_skeleton ~ ~1 ~-8 {Tags:["ed_warlord_boss","ed_boss"],CustomName:'{"text":"Ashen Warlord","color":"dark_red","bold":true}',CustomNameVisible:1b,PersistenceRequired:1b,Health:300f,Attributes:[{Name:"minecraft:generic.max_health",Base:300d},{Name:"minecraft:generic.armor_toughness",Base:6d},{Name:"minecraft:generic.knockback_resistance",Base:0.85d},{Name:"minecraft:generic.attack_damage",Base:11d},{Name:"minecraft:generic.movement_speed",Base:0.3d},{Name:"minecraft:generic.follow_range",Base:40d}],HandItems:[{id:"minecraft:netherite_sword",Count:1b,tag:{Enchantments:[{id:"minecraft:sharpness",lvl:3s},{id:"minecraft:fire_aspect",lvl:1s}]}},{}],HandDropChances:[0f,0f],ArmorItems:[{},{},{id:"minecraft:netherite_chestplate",Count:1b,tag:{Trim:{material:"minecraft:gold",pattern:"minecraft:rib"}}},{id:"minecraft:netherite_helmet",Count:1b,tag:{Trim:{material:"minecraft:redstone",pattern:"minecraft:snout"}}}],ArmorDropChances:[0f,0f,0f,0f]}
scoreboard players set @e[type=minecraft:wither_skeleton,tag=ed_warlord_boss,distance=..16] ed_phase 1
function elytra_dungeons:ashen_barrow/wave1
bossbar set elytra_dungeons:ashen_warlord players @a[distance=..48]
bossbar set elytra_dungeons:ashen_warlord value 300
bossbar set elytra_dungeons:ashen_warlord visible true
title @a[distance=..48] title {"text":"The Ashen Warlord","color":"dark_red","bold":true}
title @a[distance=..48] subtitle {"text":"has woken","color":"gray"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..48] ~ ~ ~ 1 0.6
