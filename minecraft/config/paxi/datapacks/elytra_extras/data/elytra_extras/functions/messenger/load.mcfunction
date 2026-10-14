scoreboard objectives add mes_trade minecraft.custom:minecraft.traded_with_villager
scoreboard objectives add mes_last dummy
scoreboard objectives add mes_t dummy
scoreboard objectives add mes_tm dummy
scoreboard objectives add mes_up dummy
scoreboard objectives add mes_stage dummy
scoreboard objectives add mes_answer trigger
scoreboard objectives add mes_pid dummy
scoreboard objectives add mes_vt dummy
scoreboard objectives add mes_wish dummy
scoreboard objectives add mes_price dummy
scoreboard objectives add mes_ptime dummy
scoreboard objectives add mes_pflag dummy
scoreboard objectives add mes_hp dummy
scoreboard objectives add mes_retry dummy
scoreboard objectives add mes_dth deathCount
scoreboard objectives add mes_bt dummy
# the scene (per player): owner link, timers, failsafes
scoreboard objectives add mes_owner dummy
scoreboard objectives add mes_stime dummy
scoreboard objectives add mes_mus dummy
scoreboard objectives add mes_amb dummy
scoreboard objectives add mes_wind dummy
scoreboard objectives add mes_hb dummy
scoreboard objectives add mes_leave minecraft.custom:minecraft.leave_game
scoreboard objectives add mes_sdth deathCount
scoreboard players add #hidden mes_t 0
scoreboard players set #neg mes_t -1
scoreboard players set #4 mes_t 4
scoreboard players set #6 mes_t 6
scoreboard players set #7 mes_t 7
scoreboard players set #8 mes_t 8
scoreboard players set #20 mes_t 20
scoreboard players set #32768 mes_t 32768
scoreboard players set #65536 mes_t 65536
scoreboard players set #lcg mes_t 1103515245
scoreboard players set #slots mes_t 8
scoreboard players set #amb_range mes_t 600
scoreboard players set #bell mes_t 3
scoreboard players set #max mes_stime 12000
execute unless score #rng mes_t matches -2147483648.. store result score #rng mes_t run time query gametime
scoreboard players add #next mes_pid 0
# team: lets AmbientSounds (client side) recognise the Bote and go silent near him (region elytra_bote)
team add mes_bote
execute in elytra_extras:vision run forceload add 0 0
execute in elytra_extras:vision run forceload add 1000 0
execute in elytra_extras:vision run forceload add 2000 0
execute in elytra_extras:vision run forceload add 3000 0
execute in elytra_extras:vision run forceload add 4000 0
execute in elytra_extras:vision run forceload add 5000 0
execute in elytra_extras:vision run forceload add 6000 0
execute in elytra_extras:vision run forceload add 7000 0
data modify storage elytra_extras:messenger offers set value {Recipes:[{buy:{id:"minecraft:player_head",Count:1b,tag:{SkullOwner:{Id:[I;1263553393,-1146730201,-1859123571,1047282817],Name:"Kackhaufen",Properties:{textures:[{Value:"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZGVmYmM3N2M5NzU2MDZmZGNiYzM0NzQwOWM1MmMxNmNiMWVjZThmNzQyODJjMjQ5NjhjODE3MTdkNjJiYzE3NCJ9fX0="}]}},display:{Name:'{"text":"Kackhaufen","color":"#8B5A2B","italic":false}',Lore:['{"text":"Deko. Kann auf den Boden gestellt werden.","color":"gray","italic":false}']}}},sell:{id:"minecraft:diamond",Count:1b},maxUses:9999,uses:0,rewardExp:0b,xp:0,priceMultiplier:0f,demand:0,specialPrice:0},{buy:{id:"minecraft:rotten_flesh",Count:8b},sell:{id:"minecraft:firework_rocket",Count:16b},maxUses:9999,uses:0,rewardExp:0b,xp:0,priceMultiplier:0f,demand:0,specialPrice:0},{buy:{id:"minecraft:copper_ingot",Count:4b},sell:{id:"tacz:ammo",Count:30b,tag:{AmmoId:"tacz:9mm"}},maxUses:9999,uses:0,rewardExp:0b,xp:0,priceMultiplier:0f,demand:0,specialPrice:0}]}
schedule function elytra_extras:messenger/loop 10t replace
