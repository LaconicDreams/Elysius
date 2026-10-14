tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Wissen. Ihr wollt sehen, was hinter dem Vorhang liegt? Wer seine Nase in alles steckt, macht sich Feinde. Ihr werdet sehen.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_wissen
