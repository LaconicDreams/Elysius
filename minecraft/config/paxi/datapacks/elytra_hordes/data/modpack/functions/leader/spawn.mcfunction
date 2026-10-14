# Called by horde/spawn_horde, as + at the horde's spot marker after the horde spawned.
scoreboard players set #ok ld_tmp 1
execute store result score #n ld_tmp if entity @e[tag=modpack_horde_leader,distance=..160]
execute if score #n ld_tmp matches 2.. run scoreboard players set #ok ld_tmp 0
execute if score #force ld_tmp matches 1.. run scoreboard players set #ok ld_tmp 1
execute if score #ok ld_tmp matches 1 run function modpack:leader/pick
scoreboard players set #force ld_tmp 0
