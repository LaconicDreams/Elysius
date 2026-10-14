# Every 5 seconds (100 ticks). The 5 s step is fixed: timers and cooldowns count in 5 s steps.
schedule function modpack:horde/loop 100t replace
scoreboard players remove @a[scores={mh_cd=1..}] mh_cd 5
execute if score #enabled mh_cfg matches 1 as @a[gamemode=!creative,gamemode=!spectator] at @s if dimension minecraft:overworld unless score @s mh_cd matches 1.. run function modpack:horde/player_tick
execute as @a[scores={mh_lure=1..}] at @s run function modpack:horde/lure_tick
execute as @e[type=#elytra_hordes:horde_types,tag=modpack_horde] at @s run function modpack:horde/member_tick
