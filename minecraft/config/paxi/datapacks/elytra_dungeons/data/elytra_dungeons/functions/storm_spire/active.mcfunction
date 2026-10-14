execute unless entity @a[distance=..64,gamemode=!spectator] run function elytra_dungeons:storm_spire/reset
execute if entity @s[tag=ed_active] unless entity @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96] run function elytra_dungeons:storm_spire/victory
execute if entity @s[tag=ed_active] run function elytra_dungeons:storm_spire/active_boss
