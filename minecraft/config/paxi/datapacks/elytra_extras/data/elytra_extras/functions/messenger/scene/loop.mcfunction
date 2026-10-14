# every 10 ticks, as + at a player in a scene
scoreboard players add @s mes_stime 10
effect give @s minecraft:resistance infinite 4 true
effect give @s minecraft:fire_resistance infinite 0 true
effect give @s minecraft:water_breathing infinite 0 true
execute if entity @s[tag=!mes_in_vision] run effect give @s minecraft:blindness infinite 0 true
# music: Ward while he is calm and the player is not in the vision
execute if entity @s[tag=!mes_angry,tag=!mes_in_vision] run function elytra_extras:messenger/scene/music
execute if entity @s[tag=mes_mus_on,tag=mes_angry] run function elytra_extras:messenger/scene/music_off
execute if entity @s[tag=mes_mus_on,tag=mes_in_vision] run function elytra_extras:messenger/scene/music_off
# heartbeat: off (CONFIG heartbeat.enabled)
execute if entity @s[tag=!mes_in_vision] run function elytra_extras:messenger/scene/ambient
# time limit and "is my Bote still there" (these may end the scene, so they come last)
execute if score @s mes_stime >= #max mes_stime if entity @s[tag=!mes_timeout] run function elytra_extras:messenger/scene/timeout
execute if entity @s[tag=!mes_in_vision] run function elytra_extras:messenger/scene/check_bote
execute if entity @s[tag=mes_scene] if score @s mes_stime >= #hard mes_stime run function elytra_extras:messenger/scene/end
