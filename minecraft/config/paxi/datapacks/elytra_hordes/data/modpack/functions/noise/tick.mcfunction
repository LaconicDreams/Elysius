# Every tick (#minecraft:tick). Gunfire: a TaCZ bullet entity right next to a player means that
# player just fired (functions run before entities move, so a new bullet is still at the muzzle).
scoreboard players remove @a[scores={mh_gun=1..}] mh_gun 1
execute if score #gunfire mh_cfg matches 1 as @a[gamemode=!spectator] at @s if entity @e[type=#elytra_hordes:gun_bullets,tag=!mh_heard,distance=..8] run function modpack:noise/gunshot
