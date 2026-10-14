# as a player: + #add bote_punkte points (set #add first: scoreboard players set #add bote_punkte <n>)
scoreboard players operation @s bote_punkte += #add bote_punkte
title @s actionbar ["", {"text": "+", "color": "gold"}, {"score": {"name": "#add", "objective": "bote_punkte"}, "color": "gold"}, {"text": " Gunst des Boten", "color": "gold"}]
