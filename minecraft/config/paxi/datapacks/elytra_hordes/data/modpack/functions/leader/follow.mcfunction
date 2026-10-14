scoreboard players operation #id ld_tmp = @s ld_id
execute as @e[type=minecraft:marker,tag=ld_link,distance=..64] if score @s ld_id = #id ld_tmp run tp @s ~ ~ ~
