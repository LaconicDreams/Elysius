# rebuild the Hollow arena from the current template on the next visit (use after updating the pack)
execute in elytra_dungeons:the_hollow run kill @e[type=minecraft:marker,tag=ed_hollow]
execute in elytra_dungeons:the_hollow run kill @e[type=minecraft:marker,tag=ed_rift_out]
execute in elytra_dungeons:the_hollow run kill @e[tag=ed_magus_boss]
execute in elytra_dungeons:the_hollow run kill @e[tag=ed_magus_add]
scoreboard players set #built ed_flag 0
tellraw @s {"text":"The Hollow arena will be rebuilt on the next visit.","color":"yellow"}
