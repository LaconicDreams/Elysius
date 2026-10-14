tag @s remove ed_active
tag @s add ed_idle
bossbar set elytra_dungeons:hollow_magus visible false
execute as @e[tag=ed_magus_boss,distance=..64] run data merge entity @s {DeathLootTable:"minecraft:empty"}
execute as @e[tag=ed_magus_add,distance=..64] run data merge entity @s {DeathLootTable:"minecraft:empty"}
kill @e[tag=ed_magus_boss,distance=..64]
kill @e[tag=ed_magus_add,distance=..64]
tp @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..64] ~ -300 ~
