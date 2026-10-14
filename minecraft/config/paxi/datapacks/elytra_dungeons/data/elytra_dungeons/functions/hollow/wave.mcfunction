scoreboard players set @s ed_wave 0
summon minecraft:vex ~-6 ~4 ~ {Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}
summon minecraft:vex ~6 ~4 ~ {Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}
summon minecraft:vex ~ ~4 ~-6 {Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}
execute if score @s ed_phase matches 2.. run summon minecraft:vex ~ ~4 ~6 {Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}
execute if score @s ed_phase matches 3 run summon minecraft:vex ~ ~6 ~ {Tags:["ed_add","ed_magus_add"],PersistenceRequired:1b,LifeTicks:600}
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..64] ~ ~ ~ 2 0.8
