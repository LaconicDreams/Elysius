# as a player: bote_ziel = the rank their points are worth
scoreboard players set @s bote_ziel 1
execute if score @s bote_punkte matches 0.. run scoreboard players set @s bote_ziel 1
execute if score @s bote_punkte matches 100.. run scoreboard players set @s bote_ziel 2
execute if score @s bote_punkte matches 250.. run scoreboard players set @s bote_ziel 3
execute if score @s bote_punkte matches 450.. run scoreboard players set @s bote_ziel 4
execute if score @s bote_punkte matches 700.. run scoreboard players set @s bote_ziel 5
execute if score @s bote_punkte matches 1000.. run scoreboard players set @s bote_ziel 6
execute if score @s bote_punkte matches 1400.. run scoreboard players set @s bote_ziel 7
