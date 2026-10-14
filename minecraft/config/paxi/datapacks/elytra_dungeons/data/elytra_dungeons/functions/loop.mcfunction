schedule function elytra_dungeons:loop 5t replace
# players: id for return portals, rift cooldown, deaths, Hollow void net
execute as @a unless score @s ed_pid matches 1.. run function elytra_dungeons:assign_pid
scoreboard players remove @a[scores={ed_cd=1..}] ed_cd 1
execute as @a[scores={ed_deaths=1..}] run function elytra_dungeons:hollow/on_death
execute in elytra_dungeons:the_hollow as @a[x=-300,y=-64,z=-300,dx=600,dy=134,dz=600] run function elytra_dungeons:hollow/void_net
# every boss (tag ed_boss) and the Storm Ruby join the hidden-nametag team, so Neat draws no bar on them
team join ed_bosses @e[tag=ed_boss,team=!ed_bosses]
team join ed_bosses @e[tag=ed_herald_core,team=!ed_bosses]
# dungeons
execute as @e[type=minecraft:marker,tag=ed_warlord] at @s run function elytra_dungeons:ashen_barrow/arena_tick
execute as @e[type=minecraft:marker,tag=ed_spire] at @s run function elytra_dungeons:storm_spire/arena_tick
execute as @e[type=minecraft:marker,tag=ed_resupply] at @s run function elytra_dungeons:storm_spire/resupply
execute as @e[type=minecraft:marker,tag=ed_rift_in] at @s run function elytra_dungeons:hollow/rift_in
execute as @e[type=minecraft:marker,tag=ed_rift_out] at @s run function elytra_dungeons:hollow/rift_out
execute as @e[type=minecraft:marker,tag=ed_hollow] at @s run function elytra_dungeons:hollow/arena_tick
