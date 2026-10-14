# as + at this player's return marker in the overworld
tp @a[tag=ed_returning,limit=1] ~ ~ ~
forceload remove ~ ~
scoreboard players set #found ed_tmp 1
kill @s
