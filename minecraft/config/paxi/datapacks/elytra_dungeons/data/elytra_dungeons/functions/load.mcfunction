scoreboard objectives add ed_hp dummy
scoreboard objectives add ed_phase dummy
scoreboard objectives add ed_timer dummy
scoreboard objectives add ed_wave dummy
scoreboard objectives add ed_shield dummy
scoreboard objectives add ed_tmp dummy
scoreboard objectives add ed_const dummy
scoreboard objectives add ed_flag dummy
scoreboard objectives add ed_pid dummy
scoreboard objectives add ed_cd dummy
scoreboard objectives add ed_deaths deathCount
scoreboard objectives add ed_angle dummy
scoreboard objectives add ed_fb dummy
scoreboard players set #3 ed_const 3
# boss team: hidden nametags make Neat skip boss health bars (the bossbar still shows the name)
team add ed_bosses
team modify ed_bosses nametagVisibility never
bossbar add elytra_dungeons:ashen_warlord {"text":"Ashen Warlord"}
bossbar set elytra_dungeons:ashen_warlord name {"text":"Ashen Warlord","color":"dark_red","bold":true}
bossbar set elytra_dungeons:ashen_warlord color red
bossbar set elytra_dungeons:ashen_warlord style notched_10
bossbar set elytra_dungeons:ashen_warlord max 300
bossbar set elytra_dungeons:ashen_warlord visible false
bossbar add elytra_dungeons:tempest_herald {"text":"Tempest Herald"}
bossbar set elytra_dungeons:tempest_herald name {"text":"Tempest Herald","color":"aqua","bold":true}
bossbar set elytra_dungeons:tempest_herald color blue
bossbar set elytra_dungeons:tempest_herald style notched_10
bossbar set elytra_dungeons:tempest_herald max 400
bossbar set elytra_dungeons:tempest_herald visible false
bossbar add elytra_dungeons:hollow_magus {"text":"Hollow Magus"}
bossbar set elytra_dungeons:hollow_magus name {"text":"Hollow Magus","color":"light_purple","bold":true}
bossbar set elytra_dungeons:hollow_magus color purple
bossbar set elytra_dungeons:hollow_magus style notched_10
bossbar set elytra_dungeons:hollow_magus max 500
bossbar set elytra_dungeons:hollow_magus visible false
schedule function elytra_dungeons:loop 5t replace
