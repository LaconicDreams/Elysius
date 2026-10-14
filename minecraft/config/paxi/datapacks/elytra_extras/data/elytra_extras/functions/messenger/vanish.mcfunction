# as + at the Bote's horse: smoke, gone - and his player's scene ends
tag @s add mes_leaving
particle minecraft:poof ~ ~1.2 ~ 0.7 0.9 0.7 0.05 80 force
particle minecraft:large_smoke ~ ~1.2 ~ 0.6 0.8 0.6 0.02 40 force
playsound minecraft:entity.wandering_trader.disappeared neutral @a[distance=..48] ~ ~ ~ 1.5 0.8
scoreboard players operation #own mes_pid = @s mes_owner
execute as @a[tag=mes_scene] if score @s mes_pid = #own mes_pid run function elytra_extras:messenger/scene/end
execute on passengers run kill @s
tp @s ~ -2000 ~
kill @s
