# Runs on world load and /reload (#minecraft:load). Do not run by hand: it places the world spawn
# anchor at the position it runs from (the server runs load functions at the world spawn point).
scoreboard objectives add mh_cfg dummy
scoreboard objectives add mh_const dummy
scoreboard objectives add mh_tmp dummy
scoreboard objectives add mh_timer dummy
scoreboard objectives add mh_cd dummy
scoreboard objectives add mh_lure dummy
scoreboard objectives add mh_age dummy
scoreboard objectives add mh_gun dummy
scoreboard players set #-1 mh_const -1
scoreboard players set #2 mh_const 2
scoreboard players set #3 mh_const 3
scoreboard players set #10 mh_const 10
scoreboard players set #60 mh_const 60
scoreboard players set #100 mh_const 100
function modpack:horde/settings
# derived value, do not edit here
scoreboard players operation #cooldown_s mh_cfg = #cooldown_min mh_cfg
scoreboard players operation #cooldown_s mh_cfg *= #60 mh_const
# world spawn anchor (hordes never spawn within 100 blocks of it)
kill @e[type=minecraft:marker,tag=mh_spawn]
summon minecraft:marker ~ ~ ~ {Tags:["mh_spawn"]}
schedule function modpack:horde/loop 100t replace
