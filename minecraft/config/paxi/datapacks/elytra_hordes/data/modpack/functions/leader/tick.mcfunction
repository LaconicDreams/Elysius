# Every tick: each leader's link marker follows it (the marker remembers where the leader died).
execute as @e[tag=modpack_horde_leader] at @s run function modpack:leader/follow
