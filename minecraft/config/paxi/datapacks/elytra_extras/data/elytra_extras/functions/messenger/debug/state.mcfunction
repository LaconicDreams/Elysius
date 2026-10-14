# TEST: your scene state in chat (1 = yes, 0 = no)
execute store success score #s_scene mes_t if entity @s[tag=mes_scene]
execute store success score #s_angry mes_t if entity @s[tag=mes_angry]
execute store success score #s_vision mes_t if entity @s[tag=mes_in_vision]
execute store success score #s_music mes_t if entity @s[tag=mes_mus_on]
execute store success score #s_wind mes_t if entity @s[tag=mes_wind_on]
scoreboard players set #s_seat mes_t 0
execute on vehicle if entity @s[tag=mes_seat] run scoreboard players set #s_seat mes_t 1
scoreboard players set #s_stage mes_t -1
function elytra_extras:messenger/tag_mine
execute as @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] run scoreboard players operation #s_stage mes_t = @s mes_stage
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
scoreboard players set #s_wish mes_t 0
scoreboard players set #s_price mes_t 0
execute if score @s mes_wish matches 1.. run scoreboard players operation #s_wish mes_t = @s mes_wish
execute if score @s mes_price matches 1.. run scoreboard players operation #s_price mes_t = @s mes_price
tellraw @s ["", {"text": "[Bote-Szene] ", "color": "gold"}, "Szene ", {"score": {"name": "#s_scene", "objective": "mes_t"}}, " | Zeit ", {"score": {"name": "@s", "objective": "mes_stime"}}, "/", {"score": {"name": "#max", "objective": "mes_stime"}}, " Ticks", " | Stufe ", {"score": {"name": "#s_stage", "objective": "mes_t"}}, " | wütend ", {"score": {"name": "#s_angry", "objective": "mes_t"}}, " | Vision ", {"score": {"name": "#s_vision", "objective": "mes_t"}}, " | Sitz ", {"score": {"name": "#s_seat", "objective": "mes_t"}}, " | Musik ", {"score": {"name": "#s_music", "objective": "mes_t"}}, " | Wind ", {"score": {"name": "#s_wind", "objective": "mes_t"}}, " | pid ", {"score": {"name": "@s", "objective": "mes_pid"}}, " | Wunsch ", {"score": {"name": "#s_wish", "objective": "mes_t"}}, " Preis ", {"score": {"name": "#s_price", "objective": "mes_t"}}]
