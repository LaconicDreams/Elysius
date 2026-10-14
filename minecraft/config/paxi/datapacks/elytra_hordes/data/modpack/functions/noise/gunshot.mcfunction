# As a player who just fired, at the player.
tag @e[type=#elytra_hordes:gun_bullets,tag=!mh_heard,distance=..8] add mh_heard
execute unless score @s mh_gun matches 1.. run function modpack:noise/emit_gun
