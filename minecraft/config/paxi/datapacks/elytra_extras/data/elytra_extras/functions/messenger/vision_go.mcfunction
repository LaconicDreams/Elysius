# as + at the player: remember the spot, then the vision (one block in the void), frozen in place
tag @s remove mes_vision_wait
execute unless score @s mes_pid matches 1.. run scoreboard players add #next mes_pid 1
execute unless score @s mes_pid matches 1.. run scoreboard players operation @s mes_pid = #next mes_pid
ride @s dismount
summon minecraft:marker ~ ~ ~ {Tags:["mes_return","mes_newret"]}
scoreboard players operation @e[type=minecraft:marker,tag=mes_newret,distance=..1,limit=1] mes_pid = @s mes_pid
execute as @e[type=minecraft:marker,tag=mes_newret,distance=..1] at @s run forceload add ~ ~
tag @e[type=minecraft:marker,tag=mes_newret] remove mes_newret
tag @s add mes_in_vision
function elytra_extras:messenger/scene/music_off
scoreboard players operation #slot mes_t = @s mes_pid
scoreboard players operation #slot mes_t %= #slots mes_t
execute if score #slot mes_t matches 0 run function elytra_extras:messenger/vision_slot/0
execute if score #slot mes_t matches 1 run function elytra_extras:messenger/vision_slot/1
execute if score #slot mes_t matches 2 run function elytra_extras:messenger/vision_slot/2
execute if score #slot mes_t matches 3 run function elytra_extras:messenger/vision_slot/3
execute if score #slot mes_t matches 4 run function elytra_extras:messenger/vision_slot/4
execute if score #slot mes_t matches 5 run function elytra_extras:messenger/vision_slot/5
execute if score #slot mes_t matches 6 run function elytra_extras:messenger/vision_slot/6
execute if score #slot mes_t matches 7 run function elytra_extras:messenger/vision_slot/7
effect clear @s minecraft:blindness
attribute @s minecraft:generic.movement_speed modifier add 1f2e3d4c-5b6a-4978-8695-a4b3c2d1e0f9 mes_freeze -1 multiply
effect give @s minecraft:jump_boost infinite 128 true
execute unless score #hidden mes_t matches 1 run function elytra_extras:messenger/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Seht ihr?", "color": "#FFE9A8", "italic": true, "bold": false}]
playsound minecraft:entity.wandering_trader.ambient neutral @s ~ ~ ~ 1 0.5
tellraw @s ["", {"text": "      "}, {"text": "[ JA ]", "color": "green", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger mes_answer set 31"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Antworten: JA", "color": "green"}}}]
