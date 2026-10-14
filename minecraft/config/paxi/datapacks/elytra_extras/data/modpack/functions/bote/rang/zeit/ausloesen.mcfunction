# as + at the player: enemies around are slowed, the player gets faster, cooldown starts
effect give @e[type=#modpack:bote/feindlich,distance=..12,tag=!ed_boss,tag=!modpack_horde_leader] minecraft:slowness 8 3 false
effect give @e[type=#modpack:bote/feindlich_boss,distance=..12] minecraft:slowness 8 0 false
effect give @e[tag=ed_boss,distance=..12] minecraft:slowness 8 0 false
effect give @e[tag=modpack_horde_leader,distance=..12] minecraft:slowness 8 0 false
effect give @s minecraft:speed 8 1 true
playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 1.0 0.6
particle minecraft:reverse_portal ~ ~1 ~ 4 1 4 0.02 200
scoreboard players set @s bote_cd6 3600
