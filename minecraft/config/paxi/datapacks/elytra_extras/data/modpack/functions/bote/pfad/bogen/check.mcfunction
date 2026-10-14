# as a player holding the Phoenix Bow (every tick): exactly one helper arrow if there is no other arrow
execute store result score #a bote_pfeil run clear @s minecraft:arrow 0
execute store result score #u bote_pfeil run clear @s minecraft:arrow{modpack_bogenpfeil:1b} 0
execute store result score #s bote_pfeil run clear @s minecraft:spectral_arrow 0
execute store result score #t bote_pfeil run clear @s minecraft:tipped_arrow 0
scoreboard players operation #a bote_pfeil -= #u bote_pfeil
scoreboard players operation #a bote_pfeil += #s bote_pfeil
scoreboard players operation #a bote_pfeil += #t bote_pfeil
execute if score #a bote_pfeil matches 1.. if score #u bote_pfeil matches 1.. run clear @s minecraft:arrow{modpack_bogenpfeil:1b}
execute if score #a bote_pfeil matches 0 if score #u bote_pfeil matches 0 run give @s minecraft:arrow{modpack_bogenpfeil:1b,display:{Lore:['{"text": "Pfeil des Phoenix-Bogens", "color": "gray", "italic": false}']}} 1
execute if score #a bote_pfeil matches 0 if score #u bote_pfeil matches 2.. run function modpack:bote/pfad/bogen/einer
