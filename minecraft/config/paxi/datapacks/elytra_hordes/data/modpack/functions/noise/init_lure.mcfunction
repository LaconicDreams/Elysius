# As a new lure sense: get off the carrier and take the strength from settings.
ride @s dismount
execute store result entity @s strengthpeak int 1 run scoreboard players get #lure_strength mh_cfg
tag @s remove mh_init
