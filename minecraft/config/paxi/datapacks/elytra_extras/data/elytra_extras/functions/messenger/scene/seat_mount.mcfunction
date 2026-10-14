ride @s dismount
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:armor_stand,tag=mes_seat] if score @s mes_owner = #cur mes_pid run tag @s add mes_myseat
execute unless entity @e[type=minecraft:armor_stand,tag=mes_myseat] at @s run summon minecraft:armor_stand ~ ~0.35 ~ {Tags:["mes_seat","mes_seat_new"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,DisabledSlots:4144959}
scoreboard players operation @e[type=minecraft:armor_stand,tag=mes_seat_new] mes_owner = #cur mes_pid
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] add mes_myseat
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] remove mes_seat_new
ride @s mount @e[type=minecraft:armor_stand,tag=mes_myseat,limit=1]
tag @e[type=minecraft:armor_stand,tag=mes_myseat] remove mes_myseat
