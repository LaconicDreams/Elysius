# as a player: passive abilities on or off for their rank. Fixed UUIDs: adding an existing one fails, so
# nothing stacks; health is never lowered by re-adding
execute if score @s bote_rang matches 2.. run attribute @s minecraft:generic.movement_speed modifier add 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e1 bote_rang_speed 0.1 multiply_base
execute unless score @s bote_rang matches 2.. run attribute @s minecraft:generic.movement_speed modifier remove 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e1
execute if score @s bote_rang matches 4.. run attribute @s minecraft:generic.max_health modifier add 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e2 bote_rang_leben 4 add
execute unless score @s bote_rang matches 4.. run attribute @s minecraft:generic.max_health modifier remove 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e2
execute if score @s bote_rang matches 5.. run attribute @s minecraft:generic.luck modifier add 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e3 bote_rang_luck 1 add
execute unless score @s bote_rang matches 5.. run attribute @s minecraft:generic.luck modifier remove 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e3
execute if score @s bote_rang matches 5.. run attribute @s minecraft:generic.knockback_resistance modifier add 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e4 bote_rang_knockback 0.2 add
execute unless score @s bote_rang matches 5.. run attribute @s minecraft:generic.knockback_resistance modifier remove 6b1c2d3e-4f50-4a61-8b72-93a4b5c6d7e4
