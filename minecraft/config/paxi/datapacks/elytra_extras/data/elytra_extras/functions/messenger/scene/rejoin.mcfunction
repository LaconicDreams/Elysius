# as a player who logged out and came back: a scene from before is over
scoreboard players set @s mes_leave 0
execute if entity @s[tag=mes_scene] run function elytra_extras:messenger/scene/end
