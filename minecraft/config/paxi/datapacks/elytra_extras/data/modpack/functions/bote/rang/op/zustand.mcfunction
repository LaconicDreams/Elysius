# OPERATOR: function modpack:bote/rang/op/zustand  (your own state)  or  execute as <player> run function modpack:bote/rang/op/zustand
# The text goes to that player and to everyone tagged bote_admin (once: /tag @s add bote_admin). Cooldowns in ticks.
execute if score @s bote_rang matches 1 run data modify storage modpack:bote titel set value "Sandkorn"
execute if score @s bote_rang matches 2 run data modify storage modpack:bote titel set value "Minutenzeiger"
execute if score @s bote_rang matches 3 run data modify storage modpack:bote titel set value "Stundengänger"
execute if score @s bote_rang matches 4 run data modify storage modpack:bote titel set value "Tagwandler"
execute if score @s bote_rang matches 5 run data modify storage modpack:bote titel set value "Siegelträger"
execute if score @s bote_rang matches 6 run data modify storage modpack:bote titel set value "Zeitenwandler"
execute if score @s bote_rang matches 7 run data modify storage modpack:bote titel set value "Gefährte des Boten"
tellraw @s[tag=!bote_admin] ["", {"text": "[Rang] ", "color": "gold"}, {"selector": "@s"}, ": ", {"storage": "modpack:bote", "nbt": "titel"}, " (", {"score": {"name": "@s", "objective": "bote_rang"}}, ") | Punkte ", {"score": {"name": "@s", "objective": "bote_punkte"}}, " | Ziel ", {"score": {"name": "@s", "objective": "bote_ziel"}}, " | Zeit dehnen CD ", {"score": {"name": "@s", "objective": "bote_cd6"}}, " | Atemzug CD ", {"score": {"name": "@s", "objective": "bote_cd7"}}, " | Raketen ", {"score": {"name": "@s", "objective": "bote_rkn"}}, "/", "5"]
tellraw @a[tag=bote_admin] ["", {"text": "[Rang] ", "color": "gold"}, {"selector": "@s"}, ": ", {"storage": "modpack:bote", "nbt": "titel"}, " (", {"score": {"name": "@s", "objective": "bote_rang"}}, ") | Punkte ", {"score": {"name": "@s", "objective": "bote_punkte"}}, " | Ziel ", {"score": {"name": "@s", "objective": "bote_ziel"}}, " | Zeit dehnen CD ", {"score": {"name": "@s", "objective": "bote_cd6"}}, " | Atemzug CD ", {"score": {"name": "@s", "objective": "bote_cd7"}}, " | Raketen ", {"score": {"name": "@s", "objective": "bote_rkn"}}, "/", "5"]
