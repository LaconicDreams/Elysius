scoreboard players set @s ld_t 0
playsound minecraft:entity.llama.spit hostile @a[distance=..32] ~ ~ ~ 1.5 0.6
execute anchored eyes positioned ^ ^ ^ facing entity @p[distance=..24,gamemode=!spectator] eyes run function modpack:leader/spit_throw
