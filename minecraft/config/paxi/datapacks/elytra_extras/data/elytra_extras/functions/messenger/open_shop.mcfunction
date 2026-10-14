# as + at the Bote: trades unlocked
scoreboard players set @s mes_stage 3
data modify entity @s Offers set from storage elytra_extras:messenger offers
particle minecraft:happy_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 4
title @a[tag=mes_cur] actionbar {"text": "Rechtsklick auf den Boten zum Handeln", "color": "gold"}
