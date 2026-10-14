scoreboard players set @s ed_phase 2
effect give @s minecraft:speed infinite 0 true
tellraw @a[distance=..64] {"text":"The Magus calls the Hollow's wisps!","color":"light_purple"}
function elytra_dungeons:hollow/wave
