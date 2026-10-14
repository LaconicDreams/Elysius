# OPERATOR: /function modpack:bote/force_end - ends every Bote scene at once: everyone is released,
# every Bote vanishes, seats and return markers are removed
execute as @a[tag=mes_scene] run function elytra_extras:messenger/scene/end
execute as @a[tag=mes_in_vision] run function elytra_extras:messenger/vision_back
execute as @e[type=minecraft:horse,tag=mes_horse] at @s run function elytra_extras:messenger/vanish
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] at @s run tp @s ~ -2000 ~
kill @e[type=minecraft:wandering_trader,tag=mes_npc]
kill @e[type=minecraft:armor_stand,tag=mes_seat]
execute as @e[type=minecraft:marker,tag=mes_return] at @s run function elytra_extras:messenger/return_drop
tellraw @s {"text":"Bote: alle Szenen beendet.","color":"gray"}
