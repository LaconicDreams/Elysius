# As the new Schreier leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 4
team join ld_schreier @s
effect give @s minecraft:glowing infinite 0 true
execute store result bossbar modpack:leader_schreier max run data get entity @s Health
function modpack:leader/init
