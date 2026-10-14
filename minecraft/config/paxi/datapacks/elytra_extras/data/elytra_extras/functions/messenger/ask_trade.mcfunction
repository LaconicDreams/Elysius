# as + at a player who traded
tag @s remove mes_wait
execute unless score #hidden mes_t matches 1 run function elytra_extras:messenger/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ist das alles was euer Herz begehrt?", "color": "#FFE9A8", "italic": true, "bold": false}]
playsound minecraft:entity.wandering_trader.ambient neutral @s ~ ~ ~ 1 0.7
tellraw @s ["", {"text": "      "}, {"text": "[ JA ]", "color": "green", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 1"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: JA", "color": "green"}}}, {"text": "     "}, {"text": "[ NEIN ]", "color": "red", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 2"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: NEIN", "color": "red"}}}]
