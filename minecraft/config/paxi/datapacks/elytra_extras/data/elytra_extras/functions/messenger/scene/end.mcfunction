# as a player: the scene is over (Bote gone, relog, death, time limit, force_end) - release everything
tag @s remove mes_scene
scoreboard players operation #cur mes_pid = @s mes_pid
execute if entity @s[tag=mes_in_vision] run function elytra_extras:messenger/vision_back
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function elytra_extras:messenger/return_drop
tag @s remove mes_vision_wait
ride @s dismount
execute as @e[type=minecraft:armor_stand,tag=mes_seat] if score @s mes_owner = #cur mes_pid run kill @s
effect clear @s minecraft:blindness
effect clear @s minecraft:resistance
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:water_breathing
effect clear @s minecraft:jump_boost
attribute @s minecraft:generic.movement_speed modifier remove 1f2e3d4c-5b6a-4978-8695-a4b3c2d1e0f9
function elytra_extras:messenger/scene/music_off
stopsound @s hostile minecraft:entity.warden.heartbeat
stopsound @s ambient minecraft:ambient.cave
stopsound @s ambient minecraft:block.bell.resonate
tag @s remove mes_angry
tag @s remove mes_timeout
# the wish price starts now (not during the scene)
function elytra_extras:messenger/wish/start_price
# his Bote leaves too, if he is still here
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function elytra_extras:messenger/depart
