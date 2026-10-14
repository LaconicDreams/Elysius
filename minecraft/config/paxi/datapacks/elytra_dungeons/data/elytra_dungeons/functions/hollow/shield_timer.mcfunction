# shield comes back after 15 seconds (60 loops of 5 ticks), with fresh crystals
scoreboard players add @s ed_shield 1
execute if score @s ed_shield matches 60.. run function elytra_dungeons:hollow/shield_up
