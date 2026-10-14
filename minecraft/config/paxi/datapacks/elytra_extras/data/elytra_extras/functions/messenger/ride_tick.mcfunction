tp @s ^ ^ ^0.6
execute at @s unless block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~1 ~
particle minecraft:cloud ~ ~0.1 ~ 0.3 0 0.3 0.01 2
execute if score @s mes_t matches 40 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 34 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 28 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 22 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 16 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 10 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
execute if score @s mes_t matches 4 run playsound minecraft:entity.horse.gallop neutral @a[distance=..32] ~ ~ ~ 1 1
scoreboard players remove @s mes_t 1
execute if score @s mes_t matches ..0 run function elytra_extras:messenger/vanish
