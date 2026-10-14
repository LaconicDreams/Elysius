# remove every arena marker within 32 blocks (and any running fight)
execute as @e[type=minecraft:marker,tag=ed_warlord,distance=..32] at @s run function elytra_dungeons:ashen_barrow/reset
execute as @e[type=minecraft:marker,tag=ed_spire,distance=..32] at @s run function elytra_dungeons:storm_spire/reset
kill @e[type=minecraft:marker,tag=ed_arena,tag=!ed_hollow,distance=..32]
