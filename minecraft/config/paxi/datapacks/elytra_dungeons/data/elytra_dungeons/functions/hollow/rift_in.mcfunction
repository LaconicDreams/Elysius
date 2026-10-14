# as + at a Rift Gate marker (overworld)
execute if entity @a[distance=..24] run particle minecraft:portal ~ ~1.8 ~ 0.6 1.2 0.2 0.6 25
execute if entity @a[distance=..24] run particle minecraft:reverse_portal ~ ~1.8 ~ 0.5 1.0 0.1 0.02 6
execute as @a[distance=..1.6,gamemode=!spectator,scores={ed_cd=..0}] run function elytra_dungeons:hollow/enter
