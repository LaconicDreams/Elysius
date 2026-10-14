tag @s remove ed_active
tag @s add ed_done
scoreboard players set @s ed_timer 0
bossbar set elytra_dungeons:hollow_magus visible false
execute if block ~ ~ ~2 minecraft:chest unless data block ~ ~ ~2 Items[0] run setblock ~ ~ ~2 minecraft:air
execute unless block ~ ~ ~2 minecraft:chest run setblock ~ ~ ~2 minecraft:chest[facing=south]{LootTable:"elytra_dungeons:chests/hollow_magus_reward"}
execute if data block ~ ~ ~2 Items[0] run loot spawn ~ ~1.5 ~2 loot elytra_dungeons:chests/hollow_magus_reward
loot spawn ~ ~2 ~ loot elytra_dungeons:boss/hollow_magus
advancement grant @a[distance=..64] only elytra_dungeons:bosses/hollow_magus
title @a[distance=..64] title {"text":"Magus Defeated","color":"gold","bold":true}
title @a[distance=..64] subtitle {"text":"the rift to the south leads home","color":"yellow"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..64] ~ ~ ~ 1 1
kill @e[tag=ed_magus_add,distance=..64]
tp @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..64] ~ -300 ~
