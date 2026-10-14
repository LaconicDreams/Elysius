tag @s remove ed_active
tag @s add ed_idle
bossbar set elytra_dungeons:tempest_herald visible false
execute as @e[tag=ed_herald_boss,distance=..96] run data merge entity @s {DeathLootTable:"minecraft:empty"}
execute as @e[tag=ed_herald_core,distance=..96] run data merge entity @s {Size:0,DeathLootTable:"minecraft:empty"}
execute as @e[tag=ed_herald_add,distance=..96] run data merge entity @s {DeathLootTable:"minecraft:empty"}
kill @e[tag=ed_herald_core,distance=..96]
kill @e[tag=ed_herald_boss,distance=..96]
kill @e[tag=ed_herald_add,distance=..96]
kill @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..96]
kill @e[type=minecraft:fireball,tag=ed_herald_fb,distance=..96]
kill @e[type=minecraft:marker,tag=ed_strike,distance=..96]
