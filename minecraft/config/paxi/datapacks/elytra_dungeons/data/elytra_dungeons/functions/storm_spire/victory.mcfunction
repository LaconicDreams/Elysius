tag @s remove ed_active
tag @s add ed_done
bossbar set elytra_dungeons:tempest_herald visible false
execute if block ~ ~ ~ minecraft:chest unless data block ~ ~ ~ Items[0] run setblock ~ ~ ~ minecraft:air
execute unless block ~ ~ ~ minecraft:chest run setblock ~ ~ ~ minecraft:chest[facing=south]{LootTable:"elytra_dungeons:chests/tempest_herald_reward"}
execute if data block ~ ~ ~ Items[0] run loot spawn ~ ~1.5 ~ loot elytra_dungeons:chests/tempest_herald_reward
loot spawn ~ ~2 ~ loot elytra_dungeons:boss/tempest_herald
advancement grant @a[distance=..64] only elytra_dungeons:bosses/tempest_herald
title @a[distance=..64] title {"text":"Herald Defeated","color":"gold","bold":true}
title @a[distance=..64] subtitle {"text":"the sky is quiet again","color":"yellow"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..64] ~ ~ ~ 1 1
kill @e[tag=ed_herald_add,distance=..64]
execute as @e[type=minecraft:slime,tag=ed_herald_core,distance=..96] run data merge entity @s {Size:0,DeathLootTable:"minecraft:empty"}
kill @e[type=minecraft:slime,tag=ed_herald_core,distance=..96]
kill @e[type=minecraft:item_display,tag=ed_herald_vis,distance=..96]
kill @e[type=minecraft:fireball,tag=ed_herald_fb,distance=..96]
kill @e[type=minecraft:marker,tag=ed_strike,distance=..96]
