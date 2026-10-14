# as + at a player with rank 6+ (every tick): counts sneaking ticks while holding the minecraft:clock
execute if score @s bote_snk matches 1.. if predicate modpack:bote/rang/uhr_in_hand run scoreboard players add @s bote_snc 1
execute unless score @s bote_snk matches 1.. run scoreboard players set @s bote_snc 0
execute unless predicate modpack:bote/rang/uhr_in_hand run scoreboard players set @s bote_snc 0
scoreboard players set @s bote_snk 0
execute if score @s bote_snc matches 40.. if entity @s[tag=!mes_scene] unless score @s bote_cd6 matches 1.. run function modpack:bote/rang/zeit/ausloesen
execute if score @s bote_snc matches 40.. run scoreboard players set @s bote_snc 0
