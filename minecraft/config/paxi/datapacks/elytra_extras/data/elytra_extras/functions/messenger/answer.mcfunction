# as + at a player who clicked (values: 11/12 question 1, 21 question 2, 1/2 after a trade)
# keep the button active and feedback hidden for 10 s, so double clicks / old buttons stay silent
scoreboard players set @s mes_tm 20
tag @a remove mes_cur
tag @s add mes_cur
function elytra_extras:messenger/tag_mine
execute if score @s mes_answer matches 11 as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=1},limit=1] at @s run function elytra_extras:messenger/accept
execute if score @s mes_answer matches 21 as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=2},limit=1] at @s run function elytra_extras:messenger/accept
execute if score @s mes_answer matches 12 if entity @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=1}] run function elytra_extras:messenger/punish
execute if score @s mes_answer matches 12 as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=1},limit=1] at @s run function elytra_extras:messenger/angry
execute if score @s mes_answer matches 1 as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function elytra_extras:messenger/depart
execute if score @s mes_answer matches 41 as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=4},limit=1] at @s run function elytra_extras:messenger/accept_deal
execute if score @s mes_answer matches 42 if entity @s[tag=!mes_vision_wait,tag=!mes_in_vision] if entity @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=4}] run function elytra_extras:messenger/refuse
execute if score @s mes_answer matches 31 if entity @s[tag=mes_in_vision] run function elytra_extras:messenger/vision_return
execute if score @s mes_answer matches 51..59 if entity @s[tag=!mes_has_wish] run function elytra_extras:messenger/wish/pick
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
scoreboard players set @s mes_answer 0
scoreboard players enable @s mes_answer
