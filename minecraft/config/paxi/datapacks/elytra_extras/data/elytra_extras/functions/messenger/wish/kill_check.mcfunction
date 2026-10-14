# advancement reward: this player just killed a villager or a player
advancement revoke @s only elytra_extras:bote/kill_villager
advancement revoke @s only elytra_extras:bote/kill_player
execute if score @s mes_wish matches 1 if score @s mes_price matches 1 run function elytra_extras:messenger/wish/macht_paid
