execute if entity @s[tag=ed_idle] if entity @a[distance=..9,gamemode=!spectator] run function elytra_dungeons:hollow/start
execute if entity @s[tag=ed_active] run function elytra_dungeons:hollow/active
execute if entity @s[tag=ed_done] run function elytra_dungeons:hollow/done_tick
