# Sprints while it has a target (needs line of sight to acquire one) within 24 blocks.
scoreboard players set #t ld_tmp 0
execute on target if entity @s[distance=..24] run scoreboard players set #t ld_tmp 1
execute if score #t ld_tmp matches 1 run effect give @s minecraft:speed 1 2 true
execute if score #t ld_tmp matches 1 run particle minecraft:cloud ~ ~0.2 ~ 0.2 0 0.2 0.01 2
