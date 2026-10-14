# as + at the player who refused the deal (mes_cur): blind (the scene already is), then the vision
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Lasst mich euch zeigen wo euer Schicksal liegt ohne mich.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
tag @s add mes_vision_wait
scoreboard players set @s mes_vt 6
