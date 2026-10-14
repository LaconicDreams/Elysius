# As a new gunfire sense: get off the carrier and take the strength from settings.
ride @s dismount
execute store result entity @s strengthpeak int 1 run scoreboard players get #gun_strength mh_cfg
tag @s remove mh_init
