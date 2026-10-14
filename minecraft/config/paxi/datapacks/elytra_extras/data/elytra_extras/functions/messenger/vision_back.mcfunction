# as a player in the vision: unfreeze, back to the spot they came from (their seat is still there)
function elytra_extras:messenger/vision_cleanup
tag @s add mes_returning
scoreboard players operation #cur mes_pid = @s mes_pid
scoreboard players set #found mes_t 0
execute if score #found mes_t matches 0 in minecraft:overworld as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function elytra_extras:messenger/return_here
execute if score #found mes_t matches 0 in minecraft:the_nether as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function elytra_extras:messenger/return_here
execute if score #found mes_t matches 0 in minecraft:the_end as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function elytra_extras:messenger/return_here
execute if score #found mes_t matches 0 in aether:the_aether as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function elytra_extras:messenger/return_here
execute if score #found mes_t matches 0 in minecraft:overworld run spreadplayers 0 0 0 8 false @s
tag @s remove mes_returning
