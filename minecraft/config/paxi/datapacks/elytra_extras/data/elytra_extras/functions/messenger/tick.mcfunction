execute as @e[type=minecraft:horse,tag=mes_leaving] at @s run function elytra_extras:messenger/ride_tick
# keep players in the vision on their single block
execute in elytra_extras:vision positioned 0.5 101 0.5 as @a[tag=mes_vs0,distance=0.3..] run tp @s 0.5 101 0.5
execute in elytra_extras:vision positioned 1000.5 101 0.5 as @a[tag=mes_vs1,distance=0.3..] run tp @s 1000.5 101 0.5
execute in elytra_extras:vision positioned 2000.5 101 0.5 as @a[tag=mes_vs2,distance=0.3..] run tp @s 2000.5 101 0.5
execute in elytra_extras:vision positioned 3000.5 101 0.5 as @a[tag=mes_vs3,distance=0.3..] run tp @s 3000.5 101 0.5
execute in elytra_extras:vision positioned 4000.5 101 0.5 as @a[tag=mes_vs4,distance=0.3..] run tp @s 4000.5 101 0.5
execute in elytra_extras:vision positioned 5000.5 101 0.5 as @a[tag=mes_vs5,distance=0.3..] run tp @s 5000.5 101 0.5
execute in elytra_extras:vision positioned 6000.5 101 0.5 as @a[tag=mes_vs6,distance=0.3..] run tp @s 6000.5 101 0.5
execute in elytra_extras:vision positioned 7000.5 101 0.5 as @a[tag=mes_vs7,distance=0.3..] run tp @s 7000.5 101 0.5
# the scene: back onto the seat (shift dismounts), Bote and horse face their player
execute as @e[type=minecraft:player,tag=mes_scene,tag=!mes_in_vision] run function elytra_extras:messenger/scene/seat
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] at @s run function elytra_extras:messenger/face
