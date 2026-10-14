# At a player who fired: a Zombie Awareness SOUND sense (entity zombieawareness:scent, type 1) with
# strength #gun_strength. It is summoned as the passenger of a short-lived area effect cloud, then
# dismounted. NBT keys age/strengthpeak/type read from the Zombie Awareness 1.13.1 jar (EntityScent).
summon minecraft:area_effect_cloud ~ ~ ~ {Radius:0.0f,Duration:2,WaitTime:0,Tags:["mh_carrier"],Passengers:[{id:'zombieawareness:scent',type:1,age:600,strengthpeak:40,Tags:["mh_sense","mh_gun_sense","mh_init"]}]}
execute as @e[type=#elytra_hordes:za_senses,tag=mh_init,distance=..3] run function modpack:noise/init_gun
