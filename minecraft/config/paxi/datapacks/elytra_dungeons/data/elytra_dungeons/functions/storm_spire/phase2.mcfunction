scoreboard players set @s ed_phase 2
scoreboard players set @s ed_timer 0
tellraw @a[distance=..64] {"text":"The storm breaks! Watch for sparks at your feet: lightning follows.","color":"aqua","bold":true}
playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 2 0.8
