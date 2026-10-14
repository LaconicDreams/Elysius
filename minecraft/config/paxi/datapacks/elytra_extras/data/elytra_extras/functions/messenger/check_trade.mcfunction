execute unless score @s mes_last matches -2147483648.. run scoreboard players operation @s mes_last = @s mes_trade
execute if score @s mes_trade > @s mes_last run tag @s add mes_wait
execute if score @s mes_trade > @s mes_last run scoreboard players set @s mes_t 4
scoreboard players operation @s mes_last = @s mes_trade
