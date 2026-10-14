# as + at a player who ran /trigger bote_gabe
scoreboard players set @s bote_gabe 0
execute if score @s bote_gcd matches 1.. run function modpack:bote/pfad/verlust/warten
execute unless score @s bote_gcd matches 1.. run function modpack:bote/pfad/verlust/nachgeben
