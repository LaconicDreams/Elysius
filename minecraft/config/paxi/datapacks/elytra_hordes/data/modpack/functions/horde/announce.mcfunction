# As the target player, at the player, after the horde spawned.
# shared cooldown and timer reset for everyone within 100 blocks
scoreboard players operation @a[distance=..100] mh_cd = #cooldown_s mh_cfg
scoreboard players set @a[distance=..100] mh_timer 0
title @a[distance=..100] actionbar {"text":"You hear groaning in the distance","color":"gray","italic":true}
# lure the horde towards this player (Zombie Awareness sound sense), renewed by lure_tick
scoreboard players operation @s mh_lure = #lure_s mh_cfg
function modpack:noise/lure
