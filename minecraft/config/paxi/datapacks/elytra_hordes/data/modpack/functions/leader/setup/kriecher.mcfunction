# As the new Kriecher leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 5
team join ld_kriecher @s
scale set pehkui:width 1.2 @s
scale set pehkui:height 0.45 @s
execute store result bossbar modpack:leader_kriecher max run data get entity @s Health
function modpack:leader/init
