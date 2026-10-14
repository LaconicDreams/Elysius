# as a player: puts the Bote's form of address for this player's rank into storage modpack:bote anrede
# (and bote_anr = 1..4). Use it in a line right after calling this function:
#   function modpack:bote/rang/anrede
#   tellraw @s ["",{"text":"Seid gegrüßt, "},{"storage":"modpack:bote","nbt":"anrede"},{"text":"."}]
execute if score @s bote_rang matches 1..2 run data modify storage modpack:bote anrede set value "Fremder"
execute if score @s bote_rang matches 1..2 run scoreboard players set @s bote_anr 1
execute if score @s bote_rang matches 3..4 run data modify storage modpack:bote anrede set value "Wanderer"
execute if score @s bote_rang matches 3..4 run scoreboard players set @s bote_anr 2
execute if score @s bote_rang matches 5..6 run data modify storage modpack:bote anrede set value "Siegelträger"
execute if score @s bote_rang matches 5..6 run scoreboard players set @s bote_anr 3
execute if score @s bote_rang matches 7..7 run data modify storage modpack:bote anrede set value "Gefährte"
execute if score @s bote_rang matches 7..7 run scoreboard players set @s bote_anr 4
