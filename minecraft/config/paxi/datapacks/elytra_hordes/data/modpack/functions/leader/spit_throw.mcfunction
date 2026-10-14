# At the Spucker's eyes, facing the target: a splash potion of Poison thrown along the view line with some lift.
summon minecraft:potion ^ ^ ^1 {Tags:["ld_spit_new"],Item:{id:"minecraft:splash_potion",Count:1b,tag:{CustomPotionColor:7516192,CustomPotionEffects:[{Id:19,Amplifier:0b,Duration:100}]}}}
summon minecraft:marker ^ ^ ^ {Tags:["ld_d0"]}
summon minecraft:marker ^ ^ ^1 {Tags:["ld_d1"]}
execute store result score #x0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[0] 1000
execute store result score #y0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[1] 1000
execute store result score #z0 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d0,limit=1] Pos[2] 1000
execute store result score #x1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[0] 1000
execute store result score #y1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[1] 1000
execute store result score #z1 ld_tmp run data get entity @e[type=minecraft:marker,tag=ld_d1,limit=1] Pos[2] 1000
scoreboard players operation #x1 ld_tmp -= #x0 ld_tmp
scoreboard players operation #y1 ld_tmp -= #y0 ld_tmp
scoreboard players operation #z1 ld_tmp -= #z0 ld_tmp
scoreboard players add #y1 ld_tmp 250
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[0] double 0.0014 run scoreboard players get #x1 ld_tmp
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[1] double 0.0014 run scoreboard players get #y1 ld_tmp
execute store result entity @e[type=minecraft:potion,tag=ld_spit_new,limit=1] Motion[2] double 0.0014 run scoreboard players get #z1 ld_tmp
kill @e[type=minecraft:marker,tag=ld_d0]
kill @e[type=minecraft:marker,tag=ld_d1]
tag @e[type=minecraft:potion,tag=ld_spit_new] remove ld_spit_new
