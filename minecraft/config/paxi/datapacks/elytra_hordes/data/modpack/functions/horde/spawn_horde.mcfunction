# As the spot marker, at the spot. Picks the horde kind by biome, spawns #size zombies, plays the groan.
# kind 0 = normal (zombies + some zombie villagers), 1 = dry (mostly husks), 2 = wet (some drowned)
scoreboard players set #kind mh_tmp 0
execute if biome ~ ~ ~ #forge:is_desert run scoreboard players set #kind mh_tmp 1
execute if biome ~ ~ ~ #minecraft:is_badlands run scoreboard players set #kind mh_tmp 1
execute if biome ~ ~ ~ #minecraft:is_river run scoreboard players set #kind mh_tmp 2
execute if biome ~ ~ ~ #minecraft:is_beach run scoreboard players set #kind mh_tmp 2
execute if biome ~ ~ ~ #forge:is_swamp run scoreboard players set #kind mh_tmp 2
# daytime horde (only possible with #day_hordes 1): zombies get caps so they don't burn
scoreboard players set #day mh_tmp 1
execute if predicate modpack:horde/night_or_thunder run scoreboard players set #day mh_tmp 0
scoreboard players set #i mh_tmp 0
function modpack:horde/spawn_member
function modpack:leader/spawn
# distant groan from the horde's direction (volume 5 = audible up to ~80 blocks, quiet at 40-70)
playsound minecraft:entity.zombie.ambient hostile @a[distance=..110] ~ ~1 ~ 5 0.6
playsound minecraft:entity.husk.ambient hostile @a[distance=..110] ~ ~1 ~ 5 0.5
