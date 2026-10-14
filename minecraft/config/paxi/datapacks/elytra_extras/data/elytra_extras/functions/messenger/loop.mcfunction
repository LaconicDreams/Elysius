# every 10 ticks
schedule function elytra_extras:messenger/loop 10t replace
# failsafes first: relog, death, Botes without their player, seats without a scene
execute as @a[scores={mes_leave=1..}] run function elytra_extras:messenger/scene/rejoin
execute as @a[scores={mes_sdth=1..}] run function elytra_extras:messenger/scene/died
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] run function elytra_extras:messenger/bote_check
execute as @e[type=minecraft:armor_stand,tag=mes_seat] run function elytra_extras:messenger/scene/seat_orphan
# stage 0: greeting done, question 1 after a pause
scoreboard players remove @e[type=minecraft:wandering_trader,tag=mes_npc,scores={mes_stage=0,mes_t=1..}] mes_t 1
execute as @e[type=minecraft:wandering_trader,tag=mes_npc,scores={mes_stage=0,mes_t=..0}] at @s run function elytra_extras:messenger/ask_q1
# trades (only the scene's own player, near a Bote who is open for business)
scoreboard players add @a mes_trade 0
execute as @a[tag=mes_scene] at @s if entity @e[type=minecraft:wandering_trader,tag=mes_npc,scores={mes_stage=3},distance=..8] run function elytra_extras:messenger/check_trade
execute as @a[tag=mes_scene] at @s unless entity @e[type=minecraft:wandering_trader,tag=mes_npc,scores={mes_stage=3},distance=..8] run scoreboard players operation @s mes_last = @s mes_trade
execute as @a[tag=!mes_scene] run scoreboard players operation @s mes_last = @s mes_trade
scoreboard players remove @a[scores={mes_t=1..}] mes_t 1
execute as @a[tag=mes_wait,scores={mes_t=..0}] at @s run function elytra_extras:messenger/ask_trade
# answers
execute as @a[scores={mes_answer=1..}] at @s run function elytra_extras:messenger/answer
team join mes_bote @e[type=minecraft:wandering_trader,tag=mes_npc,team=!mes_bote]
# after the farewell: leave after a short pause
scoreboard players remove @e[type=minecraft:horse,tag=mes_dwait,scores={mes_t=1..}] mes_t 1
execute as @e[type=minecraft:horse,tag=mes_dwait,scores={mes_t=..0}] at @s run function elytra_extras:messenger/wish/leave_now
# the scene: effects, music, ambient layer, time limit, Bote still there
scoreboard players operation #hard mes_stime = #max mes_stime
scoreboard players add #hard mes_stime 600
execute as @a[tag=mes_scene] at @s run function elytra_extras:messenger/scene/loop
# wind in the vision and the Hollow (everyone there)
execute as @a at @s if dimension elytra_extras:vision run function elytra_extras:messenger/wind/vision
execute as @a at @s if dimension elytra_dungeons:the_hollow run function elytra_extras:messenger/wind/hollow
execute as @a[tag=mes_wind_on] at @s unless dimension elytra_extras:vision unless dimension elytra_dungeons:the_hollow run function elytra_extras:messenger/wind/off
# wish prices (per player; timers only run while the player is online)
execute as @a[scores={mes_price=1}] at @s run function elytra_extras:messenger/wish/price_tick
execute as @a[scores={mes_hp=1}] at @s if dimension minecraft:overworld run function elytra_extras:messenger/wish/macht_horde_try
scoreboard players add @e[type=minecraft:bee,tag=bote_bienen] mes_bt 10
kill @e[type=minecraft:bee,tag=bote_bienen,scores={mes_bt=2400..}]
# the vision: blind countdown, and cleanup for anyone who left it some other way (death, /tp)
scoreboard players remove @a[tag=mes_vision_wait,scores={mes_vt=1..}] mes_vt 1
execute as @a[tag=mes_vision_wait,scores={mes_vt=..0}] at @s run function elytra_extras:messenger/vision_go
execute as @a[tag=mes_in_vision] at @s unless dimension elytra_extras:vision run function elytra_extras:messenger/vision_cleanup
# open questions expire after 60 s; command feedback returns once nobody has an open question
scoreboard players remove @a[tag=mes_asked] mes_tm 1
tag @a[tag=mes_asked,scores={mes_tm=..0}] remove mes_asked
execute if score #hidden mes_t matches 1 unless entity @a[tag=mes_asked] run function elytra_extras:messenger/feedback_on
