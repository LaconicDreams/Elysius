# as + at the player who lied: 1 heart. Resistance V would block it, so it is lifted for this one hit
effect clear @s minecraft:resistance
damage @s 2 minecraft:magic
effect give @s minecraft:resistance infinite 4 true
playsound minecraft:entity.wandering_trader.no neutral @s ~ ~ ~ 1 0.6
# one roll of thunder (weather category: not muted near the Bote); the scene keeps the player blind
playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 1 0.8
