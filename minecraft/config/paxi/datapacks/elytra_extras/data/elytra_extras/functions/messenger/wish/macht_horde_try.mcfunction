# as + at a player in the overworld who is owed a horde (retried until a valid spot is found)
scoreboard players remove @s[scores={mes_retry=1..}] mes_retry 10
execute if score @s mes_retry matches ..0 run function elytra_extras:messenger/wish/macht_horde_start
