tag @s remove ed_active
tag @s add ed_idle
bossbar set elytra_dungeons:ashen_warlord visible false
execute as @e[tag=ed_warlord_boss,distance=..96] run data merge entity @s {DeathLootTable:"minecraft:empty"}
execute as @e[tag=ed_warlord_add,distance=..64] run data merge entity @s {DeathLootTable:"minecraft:empty"}
kill @e[tag=ed_warlord_boss,distance=..96]
kill @e[tag=ed_warlord_add,distance=..64]
