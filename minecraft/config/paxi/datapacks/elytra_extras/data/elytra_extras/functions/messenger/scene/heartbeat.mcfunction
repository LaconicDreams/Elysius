scoreboard players remove @s mes_hb 10
execute if score @s mes_hb matches ..0 run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 0.6 1
execute if score @s mes_hb matches ..0 run scoreboard players set @s mes_hb 20
