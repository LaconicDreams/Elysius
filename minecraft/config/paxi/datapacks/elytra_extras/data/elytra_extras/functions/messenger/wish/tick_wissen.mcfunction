# mes_pflag: 0 waiting, 2 due (waits for overworld, away from boss arenas), 3 bees are out
execute if score @s mes_pflag matches 0 if score @s mes_ptime matches ..0 run scoreboard players set @s mes_pflag 2
execute if score @s mes_pflag matches 2 if dimension minecraft:overworld unless entity @e[type=minecraft:marker,tag=ed_arena,distance=..128] run function elytra_extras:messenger/wish/bees_go
execute if score @s mes_pflag matches 3 if score @s mes_dth matches 1.. run function elytra_extras:messenger/wish/wissen_failed
execute if score @s mes_pflag matches 3 if score @s mes_ptime matches ..0 run function elytra_extras:messenger/wish/wissen_done
