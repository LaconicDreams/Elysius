# every tick, as + at a lightning warning marker
particle minecraft:electric_spark ~ ~0.2 ~ 0.5 0.1 0.5 0.05 8
particle minecraft:end_rod ~ ~2 ~ 0.05 2 0.05 0 3
scoreboard players add @s ed_timer 1
execute if score @s ed_timer matches 20.. run summon minecraft:lightning_bolt ~ ~ ~
execute if score @s ed_timer matches 20.. run kill @s
