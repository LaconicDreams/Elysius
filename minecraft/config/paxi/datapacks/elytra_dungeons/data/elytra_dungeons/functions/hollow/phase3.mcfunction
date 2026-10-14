scoreboard players set @s ed_phase 3
scoreboard players set @s ed_timer 0
tellraw @a[distance=..64] {"text":"The void itself rejects you. Keep your wings ready!","color":"dark_purple","bold":true}
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..64] ~ ~ ~ 2 0.5
