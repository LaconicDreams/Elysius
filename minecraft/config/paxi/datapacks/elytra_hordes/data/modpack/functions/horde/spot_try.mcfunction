# As a new spot marker (summoned at the player), positioned at the player.
# Picks a random point in the ring #dist_min..#dist_max around the player, drops it to the surface
# and checks it. Keeps the marker (tag mh_spot) if good, kills it otherwise.
tag @s remove mh_spot_new
execute store result score #dx mh_tmp run data get entity @s UUID[1]
execute store result score #dz mh_tmp run data get entity @s UUID[2]
execute if score #dx mh_tmp matches ..-1 run scoreboard players operation #dx mh_tmp *= #-1 mh_const
execute if score #dz mh_tmp matches ..-1 run scoreboard players operation #dz mh_tmp *= #-1 mh_const
scoreboard players operation #span mh_tmp = #dist_max mh_cfg
scoreboard players operation #span mh_tmp *= #2 mh_const
scoreboard players add #span mh_tmp 1
scoreboard players operation #dx mh_tmp %= #span mh_tmp
scoreboard players operation #dz mh_tmp %= #span mh_tmp
scoreboard players operation #dx mh_tmp -= #dist_max mh_cfg
scoreboard players operation #dz mh_tmp -= #dist_max mh_cfg
# squared horizontal distance must lie between #dist_min^2 and #dist_max^2
scoreboard players operation #d2 mh_tmp = #dx mh_tmp
scoreboard players operation #d2 mh_tmp *= #dx mh_tmp
scoreboard players operation #t2 mh_tmp = #dz mh_tmp
scoreboard players operation #t2 mh_tmp *= #dz mh_tmp
scoreboard players operation #d2 mh_tmp += #t2 mh_tmp
scoreboard players operation #min2 mh_tmp = #dist_min mh_cfg
scoreboard players operation #min2 mh_tmp *= #dist_min mh_cfg
scoreboard players operation #max2 mh_tmp = #dist_max mh_cfg
scoreboard players operation #max2 mh_tmp *= #dist_max mh_cfg
scoreboard players set #good mh_tmp 1
execute if score #d2 mh_tmp < #min2 mh_tmp run scoreboard players set #good mh_tmp 0
execute if score #d2 mh_tmp > #max2 mh_tmp run scoreboard players set #good mh_tmp 0
# move the marker to player x/z + offset
execute store result score #px mh_tmp run data get entity @s Pos[0]
execute store result score #pz mh_tmp run data get entity @s Pos[2]
scoreboard players operation #px mh_tmp += #dx mh_tmp
scoreboard players operation #pz mh_tmp += #dz mh_tmp
execute if score #good mh_tmp matches 1 store result entity @s Pos[0] double 1 run scoreboard players get #px mh_tmp
execute if score #good mh_tmp matches 1 store result entity @s Pos[2] double 1 run scoreboard players get #pz mh_tmp
execute if score #good mh_tmp matches 1 at @s unless loaded ~ ~ ~ run scoreboard players set #good mh_tmp 0
# drop to the surface (ignores leaves, stops on water), centred on the block
execute if score #good mh_tmp matches 1 at @s align xz positioned ~0.5 ~ ~0.5 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #good mh_tmp matches 1 at @s run function modpack:horde/spot_check
execute if score #good mh_tmp matches 1 run scoreboard players set #found mh_tmp 1
execute if score #good mh_tmp matches 0 run kill @s
