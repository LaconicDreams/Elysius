# TEST/CLEANUP: /function modpack:leader/clear removes every loaded leader (no drops, no explosion).
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/despawn
kill @e[type=minecraft:marker,tag=ld_link]
bossbar set modpack:leader_laeufer visible false
bossbar set modpack:leader_spucker visible false
bossbar set modpack:leader_kriecher visible false
bossbar set modpack:leader_platzer visible false
bossbar set modpack:leader_brecher visible false
bossbar set modpack:leader_schreier visible false
