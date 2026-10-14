# as a player holding the clock: cooldown or "ready" in the action bar
execute unless score @s bote_cd6 matches 1.. run title @s actionbar {"text": "⌛ Zeit dehnen bereit (2 s schleichen)", "color": "gray"}
execute if score @s bote_cd6 matches 1.. store result score #s bote_rang run scoreboard players get @s bote_cd6
execute if score @s bote_cd6 matches 1.. run scoreboard players operation #s bote_rang /= #20 bote_rang
execute if score @s bote_cd6 matches 1.. run title @s actionbar ["", {"text": "⌛ Zeit dehnen: noch ", "color": "dark_gray"}, {"score": {"name": "#s", "objective": "bote_rang"}, "color": "dark_gray"}, {"text": " s", "color": "dark_gray"}]
