# As the new Läufer leader, at it.
tag @s remove ld_new
scoreboard players set @s ld_type 1
team join ld_laeufer @s
effect give @s minecraft:glowing infinite 0 true
execute store result bossbar modpack:leader_laeufer max run data get entity @s Health
function modpack:leader/init
