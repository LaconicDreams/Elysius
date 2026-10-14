# as + at the Magus: everyone within 7 blocks is thrown upward
scoreboard players set @s ed_timer 0
particle minecraft:reverse_portal ~ ~1 ~ 3 1 3 0.1 200
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 1 1.4
effect give @a[distance=..7,gamemode=!creative,gamemode=!spectator] minecraft:levitation 1 3 true
