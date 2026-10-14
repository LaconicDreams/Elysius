# as + at the Bote: red eyes (the invisible mark in his name switches the ETF texture), warning, question 2
function elytra_extras:messenger/tag_owner
scoreboard players set @s mes_stage 2
data merge entity @s {CustomName:'{"text": "Der Bote ", "color": "gold"}'}
particle minecraft:angry_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 6
tag @a[tag=mes_cur] add mes_angry
execute as @a[tag=mes_cur] run function elytra_extras:messenger/scene/music_off
execute as @a[tag=mes_cur] run tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ich warne euch, lügt mich nicht an, es könnte euch alles kosten. Ich frage euch - Ihr heißt ", "color": "#FFE9A8", "italic": true, "bold": false}, {"selector": "@s", "color": "#FFE9A8", "italic": true, "bold": false}, {"text": "?", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tellraw @a[tag=mes_cur] ["", {"text": "      "}, {"text": "[ JA ]", "color": "green", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 21"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: JA", "color": "green"}}}]
function elytra_extras:messenger/open_question
