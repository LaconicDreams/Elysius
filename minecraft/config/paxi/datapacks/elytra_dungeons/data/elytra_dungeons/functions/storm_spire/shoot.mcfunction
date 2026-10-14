# as the Herald, at his eyes, facing the target. Direction = (point 1 block ahead) - (eye point).
scoreboard players set @s ed_fb 0
summon minecraft:fireball ^ ^ ^3 {Tags:["ed_fb_new","ed_herald_fb"],ExplosionPower:0,power:[0.0d,0.0d,0.0d]}
summon minecraft:marker ^ ^ ^ {Tags:["ed_d0"]}
summon minecraft:marker ^ ^ ^1 {Tags:["ed_d1"]}
execute store result score #x0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[0] 1000
execute store result score #y0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[1] 1000
execute store result score #z0 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d0,limit=1] Pos[2] 1000
execute store result score #x1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[0] 1000
execute store result score #y1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[1] 1000
execute store result score #z1 ed_tmp run data get entity @e[type=minecraft:marker,tag=ed_d1,limit=1] Pos[2] 1000
scoreboard players operation #x1 ed_tmp -= #x0 ed_tmp
scoreboard players operation #y1 ed_tmp -= #y0 ed_tmp
scoreboard players operation #z1 ed_tmp -= #z0 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[0] double 0.0001 run scoreboard players get #x1 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[1] double 0.0001 run scoreboard players get #y1 ed_tmp
execute store result entity @e[type=minecraft:fireball,tag=ed_fb_new,limit=1] power[2] double 0.0001 run scoreboard players get #z1 ed_tmp
kill @e[type=minecraft:marker,tag=ed_d0]
kill @e[type=minecraft:marker,tag=ed_d1]
tag @e[type=minecraft:fireball,tag=ed_fb_new] remove ed_fb_new
playsound minecraft:entity.ghast.shoot hostile @a[distance=..64] ~ ~ ~ 2 0.8
