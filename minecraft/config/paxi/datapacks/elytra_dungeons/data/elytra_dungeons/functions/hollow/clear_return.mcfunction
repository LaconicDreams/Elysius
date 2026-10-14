scoreboard players operation #cur ed_pid = @s ed_pid
execute as @e[type=minecraft:marker,tag=ed_return] if score @s ed_pid = #cur ed_pid at @s run function elytra_dungeons:hollow/drop_return
