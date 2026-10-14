# Every 5 ticks, as + at a loaded leader.
execute store result score @s ld_hp run data get entity @s Health
execute if score @s ld_type matches 1 run bossbar set modpack:leader_laeufer players @a[distance=..48]
execute if score @s ld_type matches 1 store result bossbar modpack:leader_laeufer value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 1 run bossbar set modpack:leader_laeufer visible true
execute if score @s ld_type matches 3 run bossbar set modpack:leader_spucker players @a[distance=..48]
execute if score @s ld_type matches 3 store result bossbar modpack:leader_spucker value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 3 run bossbar set modpack:leader_spucker visible true
execute if score @s ld_type matches 5 run bossbar set modpack:leader_kriecher players @a[distance=..48]
execute if score @s ld_type matches 5 store result bossbar modpack:leader_kriecher value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 5 run bossbar set modpack:leader_kriecher visible true
execute if score @s ld_type matches 6 run bossbar set modpack:leader_platzer players @a[distance=..48]
execute if score @s ld_type matches 6 store result bossbar modpack:leader_platzer value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 6 run bossbar set modpack:leader_platzer visible true
execute if score @s ld_type matches 2 run bossbar set modpack:leader_brecher players @a[distance=..48]
execute if score @s ld_type matches 2 store result bossbar modpack:leader_brecher value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 2 run bossbar set modpack:leader_brecher visible true
execute if score @s ld_type matches 4 run bossbar set modpack:leader_schreier players @a[distance=..48]
execute if score @s ld_type matches 4 store result bossbar modpack:leader_schreier value run scoreboard players get @s ld_hp
execute if score @s ld_type matches 4 run bossbar set modpack:leader_schreier visible true
scoreboard players operation #id ld_tmp = @s ld_id
scoreboard players set #hl ld_tmp 0
execute as @e[type=minecraft:marker,tag=ld_link,distance=..64] if score @s ld_id = #id ld_tmp run scoreboard players set #hl ld_tmp 1
execute if score #hl ld_tmp matches 0 run function modpack:leader/make_link
scoreboard players remove @s[scores={ld_cue=1..}] ld_cue 5
execute if score @s ld_cue matches ..0 if entity @a[distance=..40,gamemode=!spectator] run function modpack:leader/cue
execute if score @s ld_type matches 1 run particle minecraft:dust 1.0 0.9 0.2 1.2 ~ ~1 ~ 0.35 0.6 0.35 0 3
execute if score @s ld_type matches 3 run particle minecraft:dust 0.4 1.0 0.2 1.2 ~ ~1 ~ 0.35 0.6 0.35 0 3
execute if score @s ld_type matches 6 run particle minecraft:dust 1.0 0.6 0.1 1.2 ~ ~1 ~ 0.35 0.6 0.35 0 3
execute if score @s ld_type matches 2 run particle minecraft:dust 0.8 0.1 0.1 1.2 ~ ~1 ~ 0.35 0.6 0.35 0 3
execute if score @s ld_type matches 4 run particle minecraft:dust 0.9 0.4 1.0 1.2 ~ ~1 ~ 0.35 0.6 0.35 0 3
execute if score @s ld_type matches 1 run function modpack:leader/ai/laeufer
execute if score @s ld_type matches 3 run function modpack:leader/ai/spucker
execute if score @s ld_type matches 4 run function modpack:leader/ai/schreier
execute if score @s ld_type matches 5 run function modpack:leader/ai/kriecher
execute if entity @a[distance=..64,gamemode=!spectator] run scoreboard players set @s ld_age 0
execute unless entity @a[distance=..64,gamemode=!spectator] run scoreboard players add @s ld_age 5
execute if score @s ld_age matches 3600.. run function modpack:leader/despawn
