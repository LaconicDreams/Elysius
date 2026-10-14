# TEST: the wish question right now, without the Bote (his shop will not open; the price starts at once)
tag @a remove mes_cur
tag @s add mes_cur
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Gut. Ich verlange nicht viel. Nur Dinge, die ihr ohnehin tun würdet.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Sagt mir: Wonach verlangt es euch?", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tellraw @s ["", {"text": "      "}, {"text": "[ MACHT ]", "color": "red", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 51"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: MACHT", "color": "red"}}}, {"text": "     "}, {"text": "[ SCHUTZ ]", "color": "aqua", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 52"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: SCHUTZ", "color": "aqua"}}}, {"text": "     "}, {"text": "[ WISSEN ]", "color": "light_purple", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 53"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: WISSEN", "color": "light_purple"}}}]
execute unless score #hidden mes_t matches 1 run function elytra_extras:messenger/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
