# Sets #r mh_tmp to a random number >= 0 (1.20.1 has no /random: uses a fresh marker's UUID).
summon minecraft:marker ~ ~ ~ {Tags:["mh_rng"]}
execute store result score #r mh_tmp run data get entity @e[type=minecraft:marker,tag=mh_rng,distance=..1,limit=1] UUID[0]
kill @e[type=minecraft:marker,tag=mh_rng,distance=..1]
execute if score #r mh_tmp matches ..-1 run scoreboard players operation #r mh_tmp *= #-1 mh_const
execute if score #r mh_tmp matches ..-1 run scoreboard players set #r mh_tmp 0
