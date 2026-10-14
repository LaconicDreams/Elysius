# As a horde zombie: one of three simple weapons (#w is 0..#weapon_pct-1 here).
scoreboard players operation #w mh_tmp %= #3 mh_const
execute if score #w mh_tmp matches 0 run item replace entity @s weapon.mainhand with minecraft:stone_sword
execute if score #w mh_tmp matches 1 run item replace entity @s weapon.mainhand with minecraft:iron_shovel
execute if score #w mh_tmp matches 2 run item replace entity @s weapon.mainhand with minecraft:iron_axe
