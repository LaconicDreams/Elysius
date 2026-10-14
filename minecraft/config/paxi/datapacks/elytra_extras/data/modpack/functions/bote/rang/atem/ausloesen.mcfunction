# as + at a player with very little health (rank 7+, not in a Bote scene): a short shield, then cooldown
effect give @s minecraft:absorption 10 1 false
effect give @s minecraft:resistance 5 2 false
playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.2
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.3 40
title @s actionbar {"text": "Letzter Atemzug", "color": "gold"}
scoreboard players set @s bote_cd7 12000
