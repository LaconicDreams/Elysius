# as + at a player: one rank up, with title, sound and a line from the Bote
scoreboard players add @s bote_rang 1
scoreboard players set @s bote_rwait 60
execute if score @s bote_rang matches 2 run function modpack:bote/rang/aufstieg/2
execute if score @s bote_rang matches 3 run function modpack:bote/rang/aufstieg/3
execute if score @s bote_rang matches 4 run function modpack:bote/rang/aufstieg/4
execute if score @s bote_rang matches 5 run function modpack:bote/rang/aufstieg/5
execute if score @s bote_rang matches 6 run function modpack:bote/rang/aufstieg/6
execute if score @s bote_rang matches 7 run function modpack:bote/rang/aufstieg/7
function modpack:bote/rang/faehigkeiten
# HOOK: everything that comes with a new rank (path rewards, shop, jobs) listens to this function tag
function #modpack:bote/rang_aufstieg
