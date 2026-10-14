# as the Herald: one aimed fireball every 3 s (every 2 s in phase 2)
scoreboard players add @s ed_fb 1
execute if score @s ed_phase matches 1 if score @s ed_fb matches 60.. at @s anchored eyes facing entity @p[gamemode=!spectator] eyes run function elytra_dungeons:storm_spire/shoot
execute if score @s ed_phase matches 2.. if score @s ed_fb matches 40.. at @s anchored eyes facing entity @p[gamemode=!spectator] eyes run function elytra_dungeons:storm_spire/shoot
