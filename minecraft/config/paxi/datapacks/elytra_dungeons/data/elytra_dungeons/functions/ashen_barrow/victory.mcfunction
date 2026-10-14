tag @s remove ed_active
tag @s add ed_done
bossbar set elytra_dungeons:ashen_warlord visible false
execute if block ~ ~ ~ minecraft:chest unless data block ~ ~ ~ Items[0] run setblock ~ ~ ~ minecraft:air
execute unless block ~ ~ ~ minecraft:chest run setblock ~ ~ ~ minecraft:chest[facing=south]{LootTable:"elytra_dungeons:chests/ashen_warlord_reward"}
execute if data block ~ ~ ~ Items[0] run loot spawn ~ ~1.5 ~ loot elytra_dungeons:chests/ashen_warlord_reward
loot spawn ~ ~2 ~ loot elytra_dungeons:boss/ashen_warlord
advancement grant @a[distance=..48] only elytra_dungeons:bosses/ashen_warlord
title @a[distance=..48] title {"text":"Warlord Defeated","color":"gold","bold":true}
title @a[distance=..48] subtitle {"text":"his hoard is yours","color":"yellow"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..48] ~ ~ ~ 1 1
kill @e[tag=ed_warlord_add,distance=..48]
