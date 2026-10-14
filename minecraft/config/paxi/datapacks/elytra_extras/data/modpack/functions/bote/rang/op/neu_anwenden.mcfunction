# OPERATOR: execute as <player> run function modpack:bote/rang/op/neu_anwenden   -> team and abilities for the current rank
execute if score @s bote_rang matches 1 run team join rang_1 @s
execute if score @s bote_rang matches 2 run team join rang_2 @s
execute if score @s bote_rang matches 3 run team join rang_3 @s
execute if score @s bote_rang matches 4 run team join rang_4 @s
execute if score @s bote_rang matches 5 run team join rang_5 @s
execute if score @s bote_rang matches 6 run team join rang_6 @s
execute if score @s bote_rang matches 7 run team join rang_7 @s
function modpack:bote/rang/faehigkeiten
