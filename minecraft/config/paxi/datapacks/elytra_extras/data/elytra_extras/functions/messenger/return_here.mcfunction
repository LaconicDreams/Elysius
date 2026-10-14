# as + at this player's return marker
tp @a[tag=mes_returning,limit=1] ~ ~ ~
forceload remove ~ ~
scoreboard players set #found mes_t 1
kill @s
