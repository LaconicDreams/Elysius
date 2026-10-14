# as the Herald: lower his health by #d (direct, so several hits in one moment all count)
execute store result score #b ed_tmp run data get entity @s Health
scoreboard players operation #b ed_tmp -= #d ed_tmp
execute if score #b ed_tmp matches ..0 run damage @s 9999 minecraft:generic_kill
execute if score #b ed_tmp matches 1.. store result entity @s Health float 1 run scoreboard players get #b ed_tmp
