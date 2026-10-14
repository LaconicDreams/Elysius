# As the new Brecher leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 2
team join ld_brecher @s
effect give @s minecraft:glowing infinite 0 true
scale set pehkui:base 1.25 @s
execute store result bossbar modpack:leader_brecher max run data get entity @s Health
function modpack:leader/init
