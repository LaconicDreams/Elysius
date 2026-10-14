# as the player, positioned at the gate: remember where to send them back (3 blocks out of the frame)
function elytra_dungeons:hollow/clear_return
execute positioned ~ ~ ~3 run summon minecraft:marker ~ ~ ~ {Tags:["ed_return","ed_new"]}
scoreboard players operation @e[type=minecraft:marker,tag=ed_new,limit=1] ed_pid = @s ed_pid
execute as @e[type=minecraft:marker,tag=ed_new] at @s run forceload add ~ ~
tag @e[type=minecraft:marker,tag=ed_new] remove ed_new
scoreboard players set @s ed_cd 20
effect give @s minecraft:nausea 4 0 true
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.2
tag @s add ed_to_hollow
execute if score #built ed_flag matches 1 run function elytra_dungeons:hollow/deliver
execute unless score #built ed_flag matches 1 run function elytra_dungeons:hollow/build
