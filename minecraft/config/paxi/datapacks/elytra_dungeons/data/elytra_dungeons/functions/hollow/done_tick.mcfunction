# after a win the Magus returns once nobody has been here for 10 minutes (2400 loops of 5 ticks)
execute if entity @a[distance=..80] run scoreboard players set @s ed_timer 0
execute unless entity @a[distance=..80] run scoreboard players add @s ed_timer 1
execute if score @s ed_timer matches 2400.. run function elytra_dungeons:hollow/rearm
