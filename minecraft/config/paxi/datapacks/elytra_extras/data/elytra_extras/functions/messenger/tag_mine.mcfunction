# as a player: tag this player's own Bote (the trader) mes_mine
scoreboard players operation #cur mes_pid = @s mes_pid
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] if score @s mes_owner = #cur mes_pid run tag @s add mes_mine
