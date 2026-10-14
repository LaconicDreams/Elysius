# as the player: vision spot 3 (players in the vision at the same time do not meet)
tag @s add mes_vs3
execute in elytra_extras:vision run setblock 3000 100 0 minecraft:cracked_deepslate_tiles
execute in elytra_extras:vision run tp @s 3000.5 101 0.5 0 10
