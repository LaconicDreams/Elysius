# As + at a leader: a marker that follows it every tick and notices when it is gone.
summon minecraft:marker ~ ~ ~ {Tags:["ld_link","ld_newlink"]}
scoreboard players operation @e[type=minecraft:marker,tag=ld_newlink,distance=..1,limit=1] ld_id = @s ld_id
scoreboard players operation @e[type=minecraft:marker,tag=ld_newlink,distance=..1,limit=1] ld_type = @s ld_type
tag @e[type=minecraft:marker,tag=ld_newlink] remove ld_newlink
