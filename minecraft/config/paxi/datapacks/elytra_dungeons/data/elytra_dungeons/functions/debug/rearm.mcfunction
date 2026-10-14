# restart the boss fight of every arena within 64 blocks (running, won or reset)
execute as @e[type=minecraft:marker,tag=ed_warlord,distance=..64] at @s run function elytra_dungeons:ashen_barrow/reset
execute as @e[type=minecraft:marker,tag=ed_spire,distance=..64] at @s run function elytra_dungeons:storm_spire/reset
execute as @e[type=minecraft:marker,tag=ed_hollow,distance=..64] at @s run function elytra_dungeons:hollow/reset
tag @e[type=minecraft:marker,tag=ed_arena,distance=..64] remove ed_done
tellraw @s {"text":"Arena re-armed. Step within 10 blocks of its centre to start the fight.","color":"yellow"}
