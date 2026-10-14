execute unless entity @a[distance=..64,gamemode=!spectator] run function elytra_dungeons:hollow/reset
execute if entity @s[tag=ed_active] unless entity @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..64] run function elytra_dungeons:hollow/victory
execute if entity @s[tag=ed_active] run function elytra_dungeons:hollow/active_boss
