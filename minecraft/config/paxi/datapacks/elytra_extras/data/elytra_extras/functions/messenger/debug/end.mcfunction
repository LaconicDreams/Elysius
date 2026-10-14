# TEST: end the scene the normal way: your Bote gallops off and vanishes, then you are released
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function elytra_extras:messenger/depart
