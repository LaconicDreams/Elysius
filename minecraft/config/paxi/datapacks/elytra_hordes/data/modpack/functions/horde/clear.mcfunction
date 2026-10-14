# TEST/CLEANUP: /function modpack:horde/clear removes every loaded horde zombie (no drops), this
# pack's Zombie Awareness senses and running lures. (/kill @e[tag=modpack_horde] also works, with drops.)
execute as @e[type=#elytra_hordes:horde_types,tag=modpack_horde] at @s run function modpack:horde/despawn
kill @e[type=#elytra_hordes:za_senses,tag=mh_sense]
scoreboard players reset @a mh_lure
function modpack:leader/clear
