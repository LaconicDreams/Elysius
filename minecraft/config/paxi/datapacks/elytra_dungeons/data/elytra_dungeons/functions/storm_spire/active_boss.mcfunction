bossbar set elytra_dungeons:tempest_herald players @a[distance=..64]
execute unless entity @e[type=minecraft:slime,tag=ed_herald_core,distance=..96] as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] at @s run function elytra_dungeons:storm_spire/core_respawn
execute as @e[type=minecraft:ghast,tag=ed_herald_boss,distance=..96,limit=1] run function elytra_dungeons:storm_spire/boss_tick
