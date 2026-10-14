# As a player who fired, at the player (at most once per #gun_cooldown_t ticks).
# Refreshes this pack's gunfire sense within 4 blocks, or makes a new one.
scoreboard players operation @s mh_gun = #gun_cooldown_t mh_cfg
execute as @e[type=#elytra_hordes:za_senses,tag=mh_gun_sense,distance=..4,limit=1,sort=nearest] run data merge entity @s {age:600}
execute unless entity @e[type=#elytra_hordes:za_senses,tag=mh_gun_sense,distance=..4] run function modpack:noise/new_gun_sense
