scoreboard players set @s ld_cue 160
execute if score @s ld_type matches 1 run playsound minecraft:entity.husk.ambient hostile @a[distance=..40] ~ ~ ~ 2 1.7
execute if score @s ld_type matches 3 run playsound minecraft:entity.llama.spit hostile @a[distance=..40] ~ ~ ~ 2 0.7
execute if score @s ld_type matches 5 run playsound minecraft:entity.spider.ambient hostile @a[distance=..40] ~ ~ ~ 2 0.6
execute if score @s ld_type matches 6 run playsound minecraft:entity.creeper.primed hostile @a[distance=..40] ~ ~ ~ 2 0.6
execute if score @s ld_type matches 2 run playsound minecraft:entity.ravager.step hostile @a[distance=..40] ~ ~ ~ 2 0.8
execute if score @s ld_type matches 4 run playsound minecraft:entity.zombie_villager.ambient hostile @a[distance=..40] ~ ~ ~ 2 1.6
