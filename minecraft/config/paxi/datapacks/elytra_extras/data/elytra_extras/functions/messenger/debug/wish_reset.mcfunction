# TEST: forget this player's wish and price
tag @s remove mes_has_wish
scoreboard players reset @s mes_wish
scoreboard players reset @s mes_price
scoreboard players reset @s mes_ptime
scoreboard players reset @s mes_pflag
scoreboard players reset @s mes_hp
scoreboard players reset @s mes_retry
effect clear @s minecraft:mining_fatigue
kill @e[type=minecraft:bee,tag=bote_bienen]
advancement revoke @s only elytra_extras:bote/wish_macht
advancement revoke @s only elytra_extras:bote/wish_schutz
advancement revoke @s only elytra_extras:bote/wish_wissen
advancement revoke @s only elytra_extras:bote/macht_paid
advancement revoke @s only elytra_extras:bote/macht_failed
advancement revoke @s only elytra_extras:bote/schutz_endured
advancement revoke @s only elytra_extras:bote/wissen_survived
