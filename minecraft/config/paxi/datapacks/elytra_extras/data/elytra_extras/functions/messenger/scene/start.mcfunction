# as + at the player the Bote just appeared to: the scene begins (frozen, protected, blind, music)
tag @s add mes_scene
tag @s remove mes_angry
tag @s remove mes_timeout
tag @s remove mes_mus_on
scoreboard players set @s mes_stime 0
scoreboard players set @s mes_mus 0
scoreboard players set @s mes_hb 0
scoreboard players set @s mes_amb 200
scoreboard players set @s mes_leave 0
scoreboard players set @s mes_sdth 0
ride @s dismount
function elytra_extras:messenger/tag_mine
execute facing entity @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] eyes run tp @s ~ ~ ~ ~ ~
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
summon minecraft:armor_stand ~ ~0.35 ~ {Tags:["mes_seat","mes_seat_new"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,DisabledSlots:4144959}
scoreboard players operation @e[type=minecraft:armor_stand,tag=mes_seat_new] mes_owner = @s mes_pid
ride @s mount @e[type=minecraft:armor_stand,tag=mes_seat_new,limit=1]
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] remove mes_seat_new
effect give @s minecraft:resistance infinite 4 true
effect give @s minecraft:fire_resistance infinite 0 true
effect give @s minecraft:water_breathing infinite 0 true
effect give @s minecraft:blindness infinite 0 true
