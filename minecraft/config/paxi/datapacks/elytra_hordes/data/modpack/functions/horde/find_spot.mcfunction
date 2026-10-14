# As the target player, at the player. One try per call, repeats until a spot is found or #tries runs out.
scoreboard players remove #tries mh_tmp 1
summon minecraft:marker ~ ~ ~ {Tags:["mh_spot","mh_spot_new"]}
execute as @e[type=minecraft:marker,tag=mh_spot_new,distance=..1,limit=1] run function modpack:horde/spot_try
execute if score #found mh_tmp matches 0 if score #tries mh_tmp matches 1.. run function modpack:horde/find_spot
