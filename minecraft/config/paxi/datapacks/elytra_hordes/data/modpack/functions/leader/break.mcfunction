# Horde zombies near the dead leader lose their target for 6 s, the lure towards players stops.
execute as @e[type=#elytra_hordes:horde_types,tag=modpack_horde,distance=..48] run function modpack:leader/break_one
scoreboard players reset @a[distance=..96] mh_lure
kill @e[type=#elytra_hordes:za_senses,tag=mh_lure_sense,distance=..96]
