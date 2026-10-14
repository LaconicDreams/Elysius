# As the new Spucker leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 3
team join ld_spucker @s
effect give @s minecraft:glowing infinite 0 true
execute store result bossbar modpack:leader_spucker max run data get entity @s Health
function modpack:leader/init
