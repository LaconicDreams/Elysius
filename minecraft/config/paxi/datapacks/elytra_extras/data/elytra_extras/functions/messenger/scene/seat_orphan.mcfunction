# as a seat: removed when its player is not in a scene any more
scoreboard players operation #cur mes_pid = @s mes_owner
scoreboard players set #n mes_t 0
execute as @a[tag=mes_scene] if score @s mes_pid = #cur mes_pid run scoreboard players set #n mes_t 1
execute if score #n mes_t matches 0 run kill @s
