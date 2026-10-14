# as + at the Bote
function elytra_extras:messenger/tag_owner
scoreboard players set @s mes_stage 1
execute as @a[tag=mes_cur] run tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr seid ", "color": "#FFE9A8", "italic": true, "bold": false}, {"selector": "@s", "color": "#FFE9A8", "italic": true, "bold": false}, {"text": ", richtig?", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tellraw @a[tag=mes_cur] ["", {"text": "      "}, {"text": "[ JA ]", "color": "green", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 11"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: JA", "color": "green"}}}, {"text": "     "}, {"text": "[ NEIN ]", "color": "red", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 12"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: NEIN", "color": "red"}}}]
function elytra_extras:messenger/open_question
