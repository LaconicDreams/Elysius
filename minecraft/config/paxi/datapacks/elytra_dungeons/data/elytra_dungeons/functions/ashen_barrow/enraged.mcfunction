# every 4 seconds: a ring of fire that hurts anyone within 4 blocks of the boss
scoreboard players add @s ed_timer 1
execute if score @s ed_timer matches 16.. at @s run function elytra_dungeons:ashen_barrow/fire_nova
