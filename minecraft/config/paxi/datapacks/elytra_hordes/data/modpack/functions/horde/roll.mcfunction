# As the player, at the player: one roll of #chance_pct percent.
scoreboard players set @s mh_timer 0
function modpack:horde/random
scoreboard players operation #r mh_tmp %= #100 mh_const
execute if score #r mh_tmp < #chance_pct mh_cfg run function modpack:horde/try_start
