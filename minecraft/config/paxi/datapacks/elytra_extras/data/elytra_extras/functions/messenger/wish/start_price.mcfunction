# as a player whose scene just ended: a chosen price (mes_price 4) starts running now
execute if score @s mes_price matches 4 if score @s mes_wish matches 1 run scoreboard players set @s mes_ptime 72000
execute if score @s mes_price matches 4 if score @s mes_wish matches 2 run scoreboard players set @s mes_ptime 12000
execute if score @s mes_price matches 4 if score @s mes_wish matches 2 run effect give @s minecraft:mining_fatigue infinite 0 true
execute if score @s mes_price matches 4 if score @s mes_wish matches 3 run scoreboard players set @s mes_ptime 3600
execute if score @s mes_price matches 4 run scoreboard players set @s mes_price 1
