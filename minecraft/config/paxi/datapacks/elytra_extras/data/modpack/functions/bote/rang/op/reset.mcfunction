# OPERATOR: execute as <player> run function modpack:bote/rang/op/reset   -> rank 1, 0 points, abilities off, cooldowns cleared
# (story points already earned are not given again; use op/nachtrag for that)
scoreboard players set @s bote_punkte 0
scoreboard players set @s bote_ziel 1
scoreboard players set @s bote_rang 1
scoreboard players set @s bote_rwait 0
scoreboard players set @s bote_cd6 0
scoreboard players set @s bote_cd7 0
scoreboard players set @s bote_rkn 0
team join rang_1 @s
function modpack:bote/rang/faehigkeiten
