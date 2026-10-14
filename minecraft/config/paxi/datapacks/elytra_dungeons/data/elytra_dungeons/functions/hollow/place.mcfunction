execute in elytra_dungeons:the_hollow run place template elytra_dungeons:hollow/arena -20 80 -20
execute in elytra_dungeons:the_hollow if block 0 84 12 minecraft:obsidian run scoreboard players set #built ed_flag 1
execute if score #built ed_flag matches 1 run schedule function elytra_dungeons:hollow/deliver 2t replace
execute unless score #built ed_flag matches 1 run schedule function elytra_dungeons:hollow/place 10t replace
