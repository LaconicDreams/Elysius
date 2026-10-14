# every 10 ticks, as + at a player whose price is open (mes_price 1)
scoreboard players remove @s mes_ptime 10
execute if score @s mes_wish matches 1 run function elytra_extras:messenger/wish/tick_macht
execute if score @s mes_wish matches 2 run function elytra_extras:messenger/wish/tick_schutz
execute if score @s mes_wish matches 3 run function elytra_extras:messenger/wish/tick_wissen
