# as a Bote (trader or horse): tag his player mes_cur (and #cur mes_pid = that player's id)
scoreboard players operation #cur mes_pid = @s mes_owner
tag @a remove mes_cur
execute as @a[scores={mes_pid=1..}] if score @s mes_pid = #cur mes_pid run tag @s add mes_cur
