# TEST: /function modpack:leader/here/schreier  a lone Schreier 6 blocks in front of you (no horde, ignores caps).
scoreboard players set #day mh_tmp 0
scoreboard players set #type ld_tmp 4
scoreboard players operation #last ld_last = #type ld_tmp
scoreboard players set #up ld_tmp 0
execute rotated ~ 0 positioned ^ ^ ^6 align xz positioned ~0.5 ~ ~0.5 run function modpack:leader/here_find/schreier
