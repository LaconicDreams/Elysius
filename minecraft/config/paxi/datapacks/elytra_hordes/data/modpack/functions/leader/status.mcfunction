execute store result score #n ld_tmp if entity @e[tag=modpack_horde_leader]
tellraw @s [{"text":"[Leaders] last type: ","color":"gold"},{"score":{"name":"#last","objective":"ld_last"}},{"text":" (1 Läufer, 2 Brecher, 3 Spucker, 4 Schreier, 5 Kriecher, 6 Platzer) | loaded leaders: "},{"score":{"name":"#n","objective":"ld_tmp"}}]
