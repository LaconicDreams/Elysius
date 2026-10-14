# as + at a player who just got a gift
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ein Geschenk. Behandelt es nicht gering.", "color": "#FFE9A8", "italic": true, "bold": false}]
playsound minecraft:entity.wandering_trader.ambient neutral @s ~ ~ ~ 1 0.7
execute if entity @e[type=minecraft:item,distance=..3,nbt={Age:0s,Item:{tag:{modpack_questitem:1b}}}] run tellraw @s {"text": "Euer Inventar ist voll - die Gabe liegt vor euren Füßen.", "color": "red"}
execute unless entity @s[tag=gabe_hinweis] run tellraw @s ["", {"text": "Verliert ihr eine Gabe, ruft mich: ", "color": "#FFE9A8", "italic": true}, {"text": "[Gabe zurückfordern]", "color": "gold", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger bote_gabe"}, "hoverEvent": {"action": "show_text", "contents": "/trigger bote_gabe"}}]
tag @s add gabe_hinweis
