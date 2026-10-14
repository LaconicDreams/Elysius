tag @s remove ed_shield_up
effect clear @s minecraft:resistance
effect give @s minecraft:glowing infinite 0 true
scoreboard players set @s ed_shield 0
title @a[distance=..64] actionbar {"text":"SHIELD BROKEN - shoot him now!","color":"light_purple","bold":true}
playsound minecraft:block.beacon.deactivate hostile @a[distance=..64] ~ ~ ~ 2 0.7
function elytra_dungeons:hollow/ammo_drop
