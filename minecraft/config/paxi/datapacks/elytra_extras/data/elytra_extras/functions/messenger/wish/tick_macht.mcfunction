execute if score @s mes_pflag matches 0 if score @s mes_ptime matches ..24000 run function elytra_extras:messenger/wish/macht_remind
execute if score @s mes_ptime matches ..0 run function elytra_extras:messenger/wish/macht_fail
