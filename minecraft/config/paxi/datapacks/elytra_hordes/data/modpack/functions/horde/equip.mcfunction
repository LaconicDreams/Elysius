# As a freshly spawned horde zombie. #i = its number in the horde (0 = first).
tag @s remove mh_new
scoreboard players set @s mh_age 0
execute if score #i mh_tmp < #armored mh_cfg run item replace entity @s armor.head with minecraft:iron_helmet
execute if score #i mh_tmp < #armored mh_cfg run item replace entity @s armor.chest with minecraft:iron_chestplate
execute if score #i mh_tmp < #armored mh_cfg run item replace entity @s weapon.mainhand with minecraft:iron_sword
execute store result score #w mh_tmp run data get entity @s UUID[3]
execute if score #w mh_tmp matches ..-1 run scoreboard players operation #w mh_tmp *= #-1 mh_const
scoreboard players operation #w mh_tmp %= #100 mh_const
execute if score #i mh_tmp >= #armored mh_cfg if score #w mh_tmp < #weapon_pct mh_cfg run function modpack:horde/give_weapon
execute if score #day mh_tmp matches 1 unless data entity @s ArmorItems[3].id run item replace entity @s armor.head with minecraft:leather_helmet{Unbreakable:1b}
