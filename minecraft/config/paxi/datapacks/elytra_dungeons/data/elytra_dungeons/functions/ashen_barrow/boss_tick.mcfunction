# as the boss, positioned at the arena marker
execute store result score @s ed_hp run data get entity @s Health
execute store result bossbar elytra_dungeons:ashen_warlord value run scoreboard players get @s ed_hp
execute if score @s ed_phase matches 1 if score @s ed_hp matches ..200 run function elytra_dungeons:ashen_barrow/phase2
execute if score @s ed_phase matches 2 if score @s ed_hp matches ..100 run function elytra_dungeons:ashen_barrow/phase3
execute if score @s ed_phase matches 3 run function elytra_dungeons:ashen_barrow/enraged
