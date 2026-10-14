scoreboard players set @s mes_price 2
advancement grant @s only elytra_extras:bote/macht_paid
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Das Blut klebt an euren Händen. Und ihr habt es nicht einmal bereut.", "color": "#FFE9A8", "italic": true, "bold": false}]
playsound minecraft:entity.wandering_trader.ambient neutral @s ~ ~ ~ 1 0.7
