# price not paid in time
scoreboard players set @s mes_price 3
advancement grant @s only elytra_extras:bote/macht_failed
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr habt gezögert. Meine Eintreiber kennen keine Geduld.", "color": "#FFE9A8", "italic": true, "bold": false}]
playsound minecraft:entity.wandering_trader.ambient neutral @s ~ ~ ~ 1 0.7
scoreboard players set @s mes_hp 1
scoreboard players set @s mes_retry 0
