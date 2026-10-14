# as + at the player (quest reward): the Bote appears 3 blocks ahead, on free ground
# (nothing happens while this player already has a Bote scene)
scoreboard players set #up mes_up 0
execute if entity @s[tag=!mes_scene] rotated ~ 0 positioned ^ ^ ^3 align xz positioned ~0.5 ~ ~0.5 run function elytra_extras:messenger/find
