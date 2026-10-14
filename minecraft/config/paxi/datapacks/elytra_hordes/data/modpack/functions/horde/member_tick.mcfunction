# Every 5 s, as a horde zombie (loaded chunks only), at it.
scoreboard players add @s mh_age 5
execute if score @s mh_age >= #despawn_s mh_cfg unless entity @a[gamemode=!spectator,distance=..64] run function modpack:horde/maybe_despawn
