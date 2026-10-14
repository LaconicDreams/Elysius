# uses the existing horde system (overworld only, spawn spot rules, leader with its caps / no-repeat rule)
scoreboard players reset @s mh_cd
function modpack:horde/start
execute if score @s mh_cd matches 1.. run scoreboard players set @s mes_hp 0
execute if score @s mes_hp matches 1 run scoreboard players set @s mes_retry 600
