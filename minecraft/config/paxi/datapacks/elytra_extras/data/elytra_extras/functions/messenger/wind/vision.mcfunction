# as + at a player in the vision: the wind loop
tag @s add mes_wind_on
scoreboard players remove @s mes_wind 10
execute if score @s mes_wind matches ..0 run playsound elytra_extras:wind ambient @s ~ ~ ~ 0.8 1
execute if score @s mes_wind matches ..0 run scoreboard players set @s mes_wind 1200
