# As the new Platzer leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 6
team join ld_platzer @s
effect give @s minecraft:glowing infinite 0 true
scale set pehkui:width 1.5 @s
scale set pehkui:height 1.1 @s
execute store result bossbar modpack:leader_platzer max run data get entity @s Health
function modpack:leader/init
