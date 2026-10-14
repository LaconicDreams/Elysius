# as + at the Bote (question 1 answered with JA): eyes normal (the music comes back), then the deal.
# The blindness stays for the whole scene.
function elytra_extras:messenger/tag_owner
scoreboard players set @s mes_stage 4
tag @a[tag=mes_cur] remove mes_angry
data merge entity @s {CustomName:'{"text": "Der Bote", "color": "gold"}'}
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Alleine schafft ihr es keinen Tag zu überleben. Ich biete euch einen Deal an - arbeitet für mich.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tellraw @a[tag=mes_cur] ["", {"text": "      "}, {"text": "[ JA ]", "color": "green", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 41"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: JA", "color": "green"}}}, {"text": "     "}, {"text": "[ NEIN ]", "color": "red", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 42"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: NEIN", "color": "red"}}}]
function elytra_extras:messenger/open_question
