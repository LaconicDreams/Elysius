# as + at a Bote's horse (every tick): horse and rider turn to their player's eyes
scoreboard players operation #cur mes_pid = @s mes_owner
tag @a remove mes_look
execute as @a[tag=mes_scene,tag=!mes_in_vision,distance=..16] if score @s mes_pid = #cur mes_pid run tag @s add mes_look
execute if entity @a[tag=mes_look] positioned ~ ~2.8 ~ facing entity @a[tag=mes_look,limit=1] eyes run tp @s ~ ~-2.8 ~ ~ ~
tag @s add mes_facing
execute if entity @a[tag=mes_look] on passengers run data modify entity @s Rotation set from entity @e[type=minecraft:horse,tag=mes_facing,limit=1] Rotation
tag @s remove mes_facing
execute if entity @a[tag=mes_look] at @s run tp @s ~ ~ ~ ~ 0
