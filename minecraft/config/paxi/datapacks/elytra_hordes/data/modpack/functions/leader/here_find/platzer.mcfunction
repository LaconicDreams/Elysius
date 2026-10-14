# Steps up (max 24 blocks) until there are 3 free blocks, then summons there (feet on the ground below).
execute if block ~ ~ ~ #elytra_hordes:horde_air if block ~ ~1 ~ #elytra_hordes:horde_air if block ~ ~2 ~ #elytra_hordes:horde_air run function modpack:leader/summon/platzer
execute if block ~ ~ ~ #elytra_hordes:horde_air if block ~ ~1 ~ #elytra_hordes:horde_air if block ~ ~2 ~ #elytra_hordes:horde_air run scoreboard players set #up ld_tmp 99
scoreboard players add #up ld_tmp 1
execute if score #up ld_tmp matches ..24 positioned ~ ~1 ~ run function modpack:leader/here_find/platzer
