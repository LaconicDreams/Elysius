# as the Magus, positioned at the altar marker
execute store result score @s ed_hp run data get entity @s Health
execute store result bossbar elytra_dungeons:hollow_magus value run scoreboard players get @s ed_hp
execute store result score #crystals ed_tmp if entity @e[type=minecraft:end_crystal,tag=ed_magus_crystal,distance=..32]
execute if entity @s[tag=ed_shield_up] if score #crystals ed_tmp matches 0 run function elytra_dungeons:hollow/shield_down
execute if entity @s[tag=!ed_shield_up] run function elytra_dungeons:hollow/shield_timer
execute if score @s ed_phase matches 1 if score @s ed_hp matches ..330 run function elytra_dungeons:hollow/phase2
execute if score @s ed_phase matches 2 if score @s ed_hp matches ..160 run function elytra_dungeons:hollow/phase3
scoreboard players add @s ed_wave 1
execute if score @s ed_wave matches 80.. run function elytra_dungeons:hollow/wave
execute if score @s ed_phase matches 3 run scoreboard players add @s ed_timer 1
execute if score @s ed_phase matches 3 if score @s ed_timer matches 24.. at @s run function elytra_dungeons:hollow/pulse
scoreboard players add @s ed_fb 1
execute if score @s ed_fb matches 16.. at @s facing entity @p[gamemode=!spectator] feet rotated ~ 0 positioned ~ 85 ~ run function elytra_dungeons:hollow/fangs
