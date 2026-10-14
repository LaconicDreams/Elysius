# TEST: /function elytra_extras:messenger/debug/remove   removes every Bote within 64 blocks (no drops; their scenes end)
execute as @e[type=minecraft:horse,tag=mes_horse,distance=..64] at @s run function elytra_extras:messenger/vanish
