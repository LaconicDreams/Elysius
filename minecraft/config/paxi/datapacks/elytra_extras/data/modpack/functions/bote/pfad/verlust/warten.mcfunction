scoreboard players operation #m bote_pfeil = @s bote_gcd
scoreboard players add #m bote_pfeil 1199
scoreboard players set #1200 bote_pfeil 1200
scoreboard players operation #m bote_pfeil /= #1200 bote_pfeil
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Noch nicht. Kommt in ", "color": "#FFE9A8", "italic": true, "bold": false}, {"score": {"name": "#m", "objective": "bote_pfeil"}, "color": "#FFE9A8", "italic": true, "bold": false}, {"text": " Minuten wieder.", "color": "#FFE9A8", "italic": true, "bold": false}]
