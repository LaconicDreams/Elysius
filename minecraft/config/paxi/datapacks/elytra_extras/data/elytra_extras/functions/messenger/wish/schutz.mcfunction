tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Schutz. Der Weg der Vorsichtigen. Ihr sollt ihn haben. Doch wer sich sicher fühlt, wird träge.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_schutz
