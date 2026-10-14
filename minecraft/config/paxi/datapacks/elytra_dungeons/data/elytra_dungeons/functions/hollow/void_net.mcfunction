# as a player in the Hollow who fell below y=70: back to the arrival point, a little hurt
tp @s 0.5 85 12.5 180 0
effect give @s minecraft:slow_falling 4 0 true
damage @s 4 minecraft:generic
tellraw @s {"text":"The Hollow spits you back out.","color":"dark_purple","italic":true}
