# nobody left nearby: put the fight back to sleep (no drops)
execute unless entity @a[distance=..48,gamemode=!spectator] run function elytra_dungeons:ashen_barrow/reset
# boss gone while players are here: victory
execute if entity @s[tag=ed_active] unless entity @e[type=minecraft:wither_skeleton,tag=ed_warlord_boss,distance=..96] run function elytra_dungeons:ashen_barrow/victory
execute if entity @s[tag=ed_active] run function elytra_dungeons:ashen_barrow/active_boss
