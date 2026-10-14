# every tick, as the Storm Ruby (1000 HP so it can never die and split like a normal slime):
# damage it took this tick is dealt to the Herald x3, then it heals back to full.
execute store result score @s ed_hp run data get entity @s Health
scoreboard players set #d ed_tmp 1000
scoreboard players operation #d ed_tmp -= @s ed_hp
execute if score #d ed_tmp matches 1.. run function elytra_dungeons:storm_spire/core_hit
data modify entity @s Health set value 1000f
