# as + at a resupply barrel marker: refill 4 stacks of rockets when a player is near and the barrel has none (60 s cooldown)
scoreboard players add @s ed_timer 0
scoreboard players remove @s[scores={ed_timer=1..}] ed_timer 1
execute if score @s ed_timer matches ..0 if entity @a[distance=..6] if block ~ ~ ~ minecraft:barrel unless data block ~ ~ ~ Items[{id:"minecraft:firework_rocket"}] run function elytra_dungeons:storm_spire/refill
