# every tick, but only finds something while a Herald fight runs or a lightning warning is pending
execute as @e[type=minecraft:marker,tag=ed_spire,tag=ed_active] at @s run function elytra_dungeons:storm_spire/fly
execute as @e[type=minecraft:marker,tag=ed_strike] at @s run function elytra_dungeons:storm_spire/strike_tick
