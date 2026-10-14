# As a player in the overworld without cooldown, at the player. Adds eligible time and rolls.
scoreboard players set #ok mh_tmp 0
execute if predicate modpack:horde/night_or_thunder run scoreboard players set #ok mh_tmp 1
execute if score #day_hordes mh_cfg matches 1 run scoreboard players set #ok mh_tmp 1
execute store result score #y mh_tmp run data get entity @s Pos[1]
execute if score #y mh_tmp > #max_y mh_cfg run scoreboard players set #ok mh_tmp 0
execute if score #ok mh_tmp matches 1 if score #skip_gliding mh_cfg matches 1 if entity @s[nbt={FallFlying:1b}] run scoreboard players set #ok mh_tmp 0
execute if score #ok mh_tmp matches 1 run scoreboard players add @s mh_timer 5
execute if score #ok mh_tmp matches 1 if score @s mh_timer >= #roll_every_s mh_cfg run function modpack:horde/roll
