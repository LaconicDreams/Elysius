# every tick, only for players with the active abilities
execute as @e[type=minecraft:player,scores={bote_rang=6..}] at @s run function modpack:bote/rang/zeit/check
execute as @e[type=minecraft:player,tag=!mes_scene,scores={bote_rang=7..,bote_cd7=..0,bote_hp=1..4}] at @s run function modpack:bote/rang/atem/ausloesen
