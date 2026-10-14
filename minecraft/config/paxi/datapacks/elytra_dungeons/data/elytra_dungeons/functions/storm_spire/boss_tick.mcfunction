execute store result score @s ed_hp run data get entity @s Health
execute store result bossbar elytra_dungeons:tempest_herald value run scoreboard players get @s ed_hp
execute if score @s ed_phase matches 1 if score @s ed_hp matches ..200 run function elytra_dungeons:storm_spire/phase2
scoreboard players add @s ed_wave 1
execute if score @s ed_wave matches 120.. run function elytra_dungeons:storm_spire/riders
execute if score @s ed_phase matches 2 run scoreboard players add @s ed_timer 1
execute if score @s ed_phase matches 2 if score @s ed_timer matches 20.. run function elytra_dungeons:storm_spire/lightning
