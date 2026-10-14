# Spits every 3 s at the nearest player 8-24 blocks away; backs off from players closer than 8.
scoreboard players add @s ld_t 5
execute if score @s ld_t matches 60.. if entity @p[distance=8..24,gamemode=!spectator] run function modpack:leader/spit
execute if entity @p[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 if block ^ ^ ^-1 #elytra_hordes:horde_air if block ^ ^1 ^-1 #elytra_hordes:horde_air run tp @s ^ ^ ^-0.45
