scoreboard players operation #cur mes_pid = @s mes_pid
scoreboard players set #n mes_t 0
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] if score @s mes_owner = #cur mes_pid run scoreboard players set #n mes_t 1
execute if score #n mes_t matches 0 run function elytra_extras:messenger/scene/end
