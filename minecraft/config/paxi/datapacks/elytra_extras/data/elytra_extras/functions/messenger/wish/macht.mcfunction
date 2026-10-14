tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Macht. Wie vorhersehbar, und doch so selten ehrlich ausgesprochen. Sie sei euer. Doch Macht will genährt werden: Binnen dreier Tage soll Blut fließen. Ein Dorfbewohner, oder einer euresgleichen. Ihr entscheidet.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_macht
