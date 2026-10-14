# TEST: max scene length 30 s for every scene (until the next /reload)
scoreboard players set #max mes_stime 600
tellraw @s {"text":"Bote: maximale Szenenlänge jetzt 30 s (bis /reload)","color":"gray"}
