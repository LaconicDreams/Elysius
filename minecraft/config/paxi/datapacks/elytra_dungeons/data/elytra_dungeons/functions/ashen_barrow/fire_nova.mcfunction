scoreboard players set @s ed_timer 0
particle minecraft:flame ~ ~1 ~ 2 0.4 2 0.05 120
playsound minecraft:item.firecharge.use hostile @a[distance=..24] ~ ~ ~ 1 0.7
execute as @a[distance=..4,gamemode=!creative,gamemode=!spectator] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:wither_skeleton,tag=ed_warlord_boss,limit=1,sort=nearest]
