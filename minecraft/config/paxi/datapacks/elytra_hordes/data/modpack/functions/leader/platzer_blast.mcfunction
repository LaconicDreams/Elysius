# At the spot where a Platzer died. Damage (minecraft:explosion, so armour and Blast Protection count) to
# players and to every hostile mob (horde included); no block damage unless grief_blocks is on.
particle minecraft:explosion ~ ~1 ~ 1.2 0.8 1.2 0 8 force
particle minecraft:dust 0.4 0.8 0.2 2 ~ ~1 ~ 2 1 2 0 60 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 0.9
execute as @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] run damage @s 14 minecraft:explosion
execute as @a[distance=2.5..5,gamemode=!creative,gamemode=!spectator] run damage @s 6 minecraft:explosion
execute as @e[type=#elytra_hordes:hostiles,distance=..5] run damage @s 14 minecraft:explosion
# grief_blocks is off: no block damage
