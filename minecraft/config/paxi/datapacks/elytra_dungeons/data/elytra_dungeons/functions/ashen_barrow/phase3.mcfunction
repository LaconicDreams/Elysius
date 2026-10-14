scoreboard players set @s ed_phase 3
scoreboard players set @s ed_timer 0
effect give @s minecraft:strength 999999 0 true
data merge entity @s {HasVisualFire:1b}
tellraw @a[distance=..48] {"text":"The Warlord is ENRAGED. Keep your distance!","color":"dark_red","bold":true}
playsound minecraft:entity.blaze.shoot hostile @a[distance=..48] ~ ~ ~ 2 0.5
