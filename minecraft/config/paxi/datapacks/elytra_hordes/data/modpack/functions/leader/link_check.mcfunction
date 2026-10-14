# As + at a link marker: is its leader still alive? (Health read x10; 0 = dead or gone.)
scoreboard players operation #id ld_tmp = @s ld_id
scoreboard players set #h ld_tmp 0
execute as @e[tag=modpack_horde_leader,distance=..64] if score @s ld_id = #id ld_tmp store result score #h ld_tmp run data get entity @s Health 10
execute if score #h ld_tmp matches ..0 run function modpack:leader/died
