execute as @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=16..64] run tp @s ~ ~ ~
bossbar set elytra_dungeons:hollow_magus players @a[distance=..64]
execute as @e[type=minecraft:illusioner,tag=ed_magus_boss,distance=..64,limit=1] run function elytra_dungeons:hollow/boss_tick
