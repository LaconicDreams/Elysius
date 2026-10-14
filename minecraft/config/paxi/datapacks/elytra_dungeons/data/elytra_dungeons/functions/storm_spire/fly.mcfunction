# every tick while the fight runs (as + at the arena marker): the Herald circles 10 blocks out, 11 up,
# always facing the nearest player; the core floats above his head; aimed fireballs on a timer
scoreboard players add @s ed_angle 2
execute if entity @e[type=minecraft:ghast,tag=ed_herald_boss,scores={ed_phase=2..},distance=..64] run scoreboard players add @s ed_angle 1
execute if score @s ed_angle matches 360.. run scoreboard players remove @s ed_angle 360
execute store result entity @s Rotation[0] float 1 run scoreboard players get @s ed_angle
execute rotated as @s positioned ^ ^11 ^10 as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..64,limit=1] run tp @s ~ ~ ~ facing entity @p[gamemode=!spectator] eyes
execute as @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..80] at @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..80,limit=1] run tp @s ~ ~2 ~ ~ 0
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80] at @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..80,limit=1] rotated ~ 0 positioned ~ ~2 ~ positioned ^ ^1.25 ^2.35 run tp @s ~ ~-0.52 ~
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80] at @s run particle minecraft:dust 1.0 0.1 0.15 1.2 ~ ~0.52 ~ 0.25 0.25 0.25 0 2
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..80,limit=1] run function elytra_dungeons:storm_spire/core_tick
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..64,limit=1] run function elytra_dungeons:storm_spire/fire_timer
