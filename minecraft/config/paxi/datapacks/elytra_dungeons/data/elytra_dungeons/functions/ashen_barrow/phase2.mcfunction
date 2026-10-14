scoreboard players set @s ed_phase 2
effect give @s minecraft:speed 999999 0 true
tellraw @a[distance=..48] {"text":"The Warlord calls his guard!","color":"red"}
playsound minecraft:entity.wither_skeleton.ambient hostile @a[distance=..48] ~ ~ ~ 2 0.5
function elytra_dungeons:ashen_barrow/wave2
