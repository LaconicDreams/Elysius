# as the Herald, at the arena marker: mark a random player's spot; the strike lands 1 s later
scoreboard players set @s ed_timer 0
execute at @r[distance=..48,gamemode=!spectator] run summon minecraft:marker ~ ~ ~ {Tags:["ed_strike"]}
