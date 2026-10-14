scoreboard players operation #d ed_tmp *= #3 ed_const
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] run function elytra_dungeons:storm_spire/core_apply
execute at @s run particle minecraft:electric_spark ~ ~0.5 ~ 0.6 0.6 0.6 0.3 30
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @a[distance=..64] ~ ~ ~ 1.5 1.6
