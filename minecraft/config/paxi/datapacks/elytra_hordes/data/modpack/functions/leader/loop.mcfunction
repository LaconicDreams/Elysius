# Every 5 ticks; only loaded leaders, link markers and briefly "broken" horde zombies are touched.
schedule function modpack:leader/loop 5t replace
execute as @e[type=minecraft:marker,tag=ld_link] at @s run function modpack:leader/link_check
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/leader_tick
execute as @e[tag=ld_broken] run function modpack:leader/broken_tick
