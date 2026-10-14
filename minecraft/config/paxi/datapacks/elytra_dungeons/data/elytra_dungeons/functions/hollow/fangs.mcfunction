# a line of evoker fangs racing toward the nearest player (arena floor surface is y=85)
scoreboard players set @s ed_fb 0
summon minecraft:evoker_fangs ^ ^ ^2 {Warmup:0}
summon minecraft:evoker_fangs ^ ^ ^3.5 {Warmup:2}
summon minecraft:evoker_fangs ^ ^ ^5 {Warmup:4}
summon minecraft:evoker_fangs ^ ^ ^6.5 {Warmup:6}
summon minecraft:evoker_fangs ^ ^ ^8 {Warmup:8}
summon minecraft:evoker_fangs ^ ^ ^9.5 {Warmup:10}
summon minecraft:evoker_fangs ^ ^ ^11 {Warmup:12}
summon minecraft:evoker_fangs ^ ^ ^12.5 {Warmup:14}
summon minecraft:evoker_fangs ^ ^ ^14 {Warmup:16}
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..48] ~ ~ ~ 1.5 0.8
