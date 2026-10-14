# as a player whose scene reached the max length: he says the line and leaves
tag @s add mes_timeout
execute if entity @s[tag=mes_in_vision] run function elytra_extras:messenger/vision_back
tag @s remove mes_vision_wait
tag @a remove mes_cur
tag @s add mes_cur
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Die Zeit drängt. Ich muss weiter.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function elytra_extras:messenger/depart
