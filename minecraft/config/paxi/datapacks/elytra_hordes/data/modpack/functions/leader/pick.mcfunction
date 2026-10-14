execute if score #force ld_tmp matches 1.. run scoreboard players operation #type ld_tmp = #force ld_tmp
scoreboard players set #tries ld_tmp 0
execute unless score #force ld_tmp matches 1.. run function modpack:leader/roll
scoreboard players operation #last ld_last = #type ld_tmp
function modpack:leader/spawn_type
