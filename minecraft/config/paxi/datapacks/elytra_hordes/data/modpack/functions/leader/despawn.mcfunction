# As + at a leader: removed without drops and without death effects.
scoreboard players operation #id ld_tmp = @s ld_id
execute as @e[type=minecraft:marker,tag=ld_link] if score @s ld_id = #id ld_tmp run function modpack:leader/unlink
data merge entity @s {DeathLootTable:"minecraft:empty"}
tp @s ~ -2000 ~
kill @s
