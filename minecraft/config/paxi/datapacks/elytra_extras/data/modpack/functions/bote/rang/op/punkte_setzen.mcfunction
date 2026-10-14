# OPERATOR: scoreboard players set #wert bote_punkte <n>  then  execute as <player> run function modpack:bote/rang/op/punkte_setzen
# (or simply: /scoreboard players set <player> bote_punkte <n>; the rank follows within half a second)
scoreboard players operation @s bote_punkte = #wert bote_punkte
