execute if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable if block ~ ~2 ~ #minecraft:replaceable run function elytra_extras:messenger/appear
execute if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable if block ~ ~2 ~ #minecraft:replaceable run scoreboard players set #up mes_up 99
scoreboard players add #up mes_up 1
execute if score #up mes_up matches ..24 positioned ~ ~1 ~ run function elytra_extras:messenger/find
