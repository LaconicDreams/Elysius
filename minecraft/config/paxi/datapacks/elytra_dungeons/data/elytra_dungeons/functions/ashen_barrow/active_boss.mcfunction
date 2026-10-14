# keep the boss inside the arena
execute as @e[type=minecraft:wither_skeleton,tag=ed_warlord_boss,distance=18..96] run tp @s ~ ~1 ~
bossbar set elytra_dungeons:ashen_warlord players @a[distance=..48]
execute as @e[type=minecraft:wither_skeleton,tag=ed_warlord_boss,distance=..96,limit=1] run function elytra_dungeons:ashen_barrow/boss_tick
