# Ward for this player only, from the start (a sound cannot resume mid-track)
stopsound @s music
playsound minecraft:music_disc.ward record @s ~ ~ ~ 0.35 1
scoreboard players set @s mes_mus 5030
