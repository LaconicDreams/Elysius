# Screams every 15 s (while a player is within 32 blocks) and calls 2 zombies, at most 6 in total.
# Unsuppressed gunfire within 32 blocks makes it scream sooner.
scoreboard players add @s ld_t 5
execute if entity @a[distance=..32,scores={mh_gun=1..},predicate=!modpack:leader/suppressed] run scoreboard players add @s ld_t 20
execute if score @s ld_t matches 300.. if score @s ld_sum matches ..5 if entity @a[distance=..32,gamemode=!spectator] run function modpack:leader/scream
