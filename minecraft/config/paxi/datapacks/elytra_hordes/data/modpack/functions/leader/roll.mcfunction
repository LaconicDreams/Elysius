# Weighted pick (total weight 100); re-rolls up to 8 times if it equals the last type, then takes the next type.
function modpack:horde/random
scoreboard players operation #p ld_tmp = #r mh_tmp
scoreboard players set #w ld_tmp 100
scoreboard players operation #p ld_tmp %= #w ld_tmp
execute if score #p ld_tmp matches 0..29 run scoreboard players set #type ld_tmp 1
execute if score #p ld_tmp matches 30..49 run scoreboard players set #type ld_tmp 3
execute if score #p ld_tmp matches 50..64 run scoreboard players set #type ld_tmp 5
execute if score #p ld_tmp matches 65..79 run scoreboard players set #type ld_tmp 6
execute if score #p ld_tmp matches 80..89 run scoreboard players set #type ld_tmp 2
execute if score #p ld_tmp matches 90..99 run scoreboard players set #type ld_tmp 4
scoreboard players add #tries ld_tmp 1
execute if score #type ld_tmp = #last ld_last if score #tries ld_tmp matches ..8 run function modpack:leader/roll
execute if score #type ld_tmp = #last ld_last run scoreboard players operation #type ld_tmp %= #6 ld_tmp
execute if score #type ld_tmp = #last ld_last run scoreboard players add #type ld_tmp 1
