# first visit in this world: load the arena area and place the arena
execute in elytra_dungeons:the_hollow run forceload add -32 -32 31 31
tellraw @a[tag=ed_to_hollow] {"text":"The rift tears open...","color":"light_purple","italic":true}
schedule function elytra_dungeons:hollow/place 10t replace
