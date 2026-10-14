# At the horde's target player: a Zombie Awareness SOUND sense with strength #lure_strength, so
# zombies (Zombie Awareness enhancedMobs) that are not busy path towards this spot.
summon minecraft:area_effect_cloud ~ ~ ~ {Radius:0.0f,Duration:2,WaitTime:0,Tags:["mh_carrier"],Passengers:[{id:'zombieawareness:scent',type:1,age:600,strengthpeak:150,Tags:["mh_sense","mh_lure_sense","mh_init"]}]}
execute as @e[type=#elytra_hordes:za_senses,tag=mh_init,distance=..3] run function modpack:noise/init_lure
