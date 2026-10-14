# every 10 ticks
schedule function modpack:bote/rang/loop 10t replace
# new players: rank 1, 0 points
execute as @a unless score @s bote_punkte matches -2147483648.. run scoreboard players set @s bote_punkte 0
execute as @a unless score @s bote_rang matches 1.. run scoreboard players set @s bote_rang 1
scoreboard players add @a bote_cd6 0
scoreboard players add @a bote_cd7 0
# rank from points; going up one rank at a time with the ceremony (not during a Bote scene), down at once
execute as @a run function modpack:bote/rang/ziel
scoreboard players remove @a[scores={bote_rwait=1..}] bote_rwait 10
execute as @a[tag=!mes_scene] if score @s bote_rang < @s bote_ziel unless score @s bote_rwait matches 1.. at @s run function modpack:bote/rang/aufstieg
execute as @a if score @s bote_rang > @s bote_ziel run function modpack:bote/rang/abstieg
execute as @a[scores={bote_rang=1},team=!rang_1] run team join rang_1 @s
execute as @a[scores={bote_rang=2},team=!rang_2] run team join rang_2 @s
execute as @a[scores={bote_rang=3},team=!rang_3] run team join rang_3 @s
execute as @a[scores={bote_rang=4},team=!rang_4] run team join rang_4 @s
execute as @a[scores={bote_rang=5},team=!rang_5] run team join rang_5 @s
execute as @a[scores={bote_rang=6},team=!rang_6] run team join rang_6 @s
execute as @a[scores={bote_rang=7},team=!rang_7] run team join rang_7 @s
# abilities (passive ones are checked every time: login, respawn, rank change all covered)
execute as @e[type=minecraft:player] run function modpack:bote/rang/faehigkeiten
execute as @e[type=minecraft:player,tag=!mes_scene,scores={bote_rang=3..,bote_rkt=1..}] at @s run function modpack:bote/rang/rakete
scoreboard players set @a bote_rkt 0
scoreboard players remove @a[scores={bote_cd6=1..}] bote_cd6 10
scoreboard players remove @a[scores={bote_cd7=1..}] bote_cd7 10
execute as @a[scores={bote_rang=6..},predicate=modpack:bote/rang/uhr_in_hand] run function modpack:bote/rang/zeit/anzeige
