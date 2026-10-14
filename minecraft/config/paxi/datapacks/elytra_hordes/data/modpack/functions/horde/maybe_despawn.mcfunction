# As an old horde zombie with no player within 64 blocks: removed unless it has an attack target.
scoreboard players set #t mh_tmp 0
execute on target run scoreboard players set #t mh_tmp 1
execute if score #t mh_tmp matches 0 run function modpack:horde/despawn
