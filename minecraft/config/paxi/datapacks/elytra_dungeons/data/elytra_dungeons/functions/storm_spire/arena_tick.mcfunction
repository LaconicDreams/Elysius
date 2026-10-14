execute if entity @s[tag=ed_idle] if entity @a[distance=..20,gamemode=!spectator] run function elytra_dungeons:storm_spire/start
execute if entity @s[tag=ed_active] run function elytra_dungeons:storm_spire/active
