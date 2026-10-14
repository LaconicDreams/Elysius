# as the player, at the free spot: the Bote (owned by this player), then the scene starts
execute unless score @s mes_pid matches 1.. run scoreboard players add #next mes_pid 1
execute unless score @s mes_pid matches 1.. run scoreboard players operation @s mes_pid = #next mes_pid
tag @a remove mes_cur
tag @s add mes_cur
summon minecraft:horse ~ ~ ~ {Tags:["mes_horse","mes_new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Tame:1b,Variant:4,SaddleItem:{id:"minecraft:saddle",Count:1b},Passengers:[{id:"minecraft:wandering_trader",Tags:["mes_npc","mes_npc_new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CustomName:'{"text": "Der Bote", "color": "gold"}',CustomNameVisible:1b,Offers:{Recipes:[]}}]}
scoreboard players operation @e[type=minecraft:horse,tag=mes_new] mes_owner = @s mes_pid
scoreboard players operation @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_owner = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_new,limit=1,sort=nearest,distance=..2] at @s run tp @s ~ ~ ~ facing entity @a[tag=mes_cur,limit=1]
tag @e[type=minecraft:horse,tag=mes_new] remove mes_new
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_stage 0
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_t 4
team join mes_bote @e[type=minecraft:wandering_trader,tag=mes_npc_new]
tag @e[type=minecraft:wandering_trader,tag=mes_npc_new] remove mes_npc_new
particle minecraft:poof ~ ~1.2 ~ 0.7 0.9 0.7 0.05 60 force
playsound minecraft:entity.wandering_trader.reappeared neutral @a[distance=..48] ~ ~ ~ 1.5 0.8
execute at @s run function elytra_extras:messenger/scene/start
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Seid gegrüßt. Ein Bad würde euch guttun.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
