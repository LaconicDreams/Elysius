# As a new leader, at it: id, timers, daytime cap, link marker.
scoreboard players add #next ld_id 1
scoreboard players operation @s ld_id = #next ld_id
scoreboard players set @s ld_age 0
scoreboard players set @s ld_t 0
scoreboard players set @s ld_sum 0
scoreboard players set @s ld_cue 0
execute if score #day mh_tmp matches 1 unless data entity @s ArmorItems[3].id run item replace entity @s armor.head with minecraft:leather_helmet{Unbreakable:1b}
function modpack:leader/make_link
