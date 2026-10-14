# one quiet cave sound or a distant low bell, then a random pause (random numbers: scoreboard LCG + game time)
scoreboard players operation #rng mes_t *= #lcg mes_t
scoreboard players add #rng mes_t 12345
execute store result score #gt mes_t run time query gametime
scoreboard players operation #rng mes_t += #gt mes_t
scoreboard players operation #x mes_t = #rng mes_t
scoreboard players operation #x mes_t /= #65536 mes_t
scoreboard players operation #x mes_t %= #32768 mes_t
scoreboard players operation @s mes_amb = #x mes_t
scoreboard players operation @s mes_amb %= #amb_range mes_t
scoreboard players add @s mes_amb 300
scoreboard players operation #y mes_t = #x mes_t
scoreboard players operation #y mes_t /= #7 mes_t
scoreboard players operation #y mes_t %= #bell mes_t
scoreboard players operation #d mes_t = #x mes_t
scoreboard players operation #d mes_t %= #4 mes_t
execute if score #y mes_t matches 1.. run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.3 1.0
execute if score #y mes_t matches 0 if score #d mes_t matches 0 rotated 0 0 positioned ^ ^ ^8 run playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 1.0 0.5
execute if score #y mes_t matches 0 if score #d mes_t matches 1 rotated 90 0 positioned ^ ^ ^8 run playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 1.0 0.5
execute if score #y mes_t matches 0 if score #d mes_t matches 2 rotated 180 0 positioned ^ ^ ^8 run playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 1.0 0.5
execute if score #y mes_t matches 0 if score #d mes_t matches 3 rotated 270 0 positioned ^ ^ ^8 run playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 1.0 0.5
