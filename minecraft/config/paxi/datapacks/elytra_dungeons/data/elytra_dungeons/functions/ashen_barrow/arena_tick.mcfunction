# as + at an Ashen Barrow arena marker, every 5 ticks
execute if entity @s[tag=ed_idle] if entity @a[distance=..10,gamemode=!spectator] run function elytra_dungeons:ashen_barrow/start
execute if entity @s[tag=ed_active] run function elytra_dungeons:ashen_barrow/active
