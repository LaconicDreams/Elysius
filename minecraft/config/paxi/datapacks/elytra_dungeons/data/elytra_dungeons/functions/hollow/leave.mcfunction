tag @s add ed_returning
scoreboard players operation #cur ed_pid = @s ed_pid
scoreboard players set #found ed_tmp 0
execute as @e[type=minecraft:marker,tag=ed_return] if score @s ed_pid = #cur ed_pid at @s run function elytra_dungeons:hollow/return_here
execute if score #found ed_tmp matches 0 in minecraft:overworld run spreadplayers 0 0 0 8 false @s
effect give @s minecraft:slow_falling 5 0 true
scoreboard players set @s ed_cd 20
tag @s remove ed_returning
