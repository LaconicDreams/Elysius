# Runs on load (#minecraft:load). Leader teams hide nametags, which also makes Neat skip their health bar.
scoreboard objectives add ld_id dummy
scoreboard objectives add ld_type dummy
scoreboard objectives add ld_hp dummy
scoreboard objectives add ld_t dummy
scoreboard objectives add ld_age dummy
scoreboard objectives add ld_sum dummy
scoreboard objectives add ld_cue dummy
scoreboard objectives add ld_tmp dummy
scoreboard objectives add ld_last dummy
scoreboard objectives add ld_brk dummy
scoreboard players set #6 ld_tmp 6
scoreboard players add #next ld_id 0
scoreboard players add #last ld_last 0
scoreboard players set #force ld_tmp 0
team add ld_laeufer
team modify ld_laeufer color yellow
team modify ld_laeufer nametagVisibility never
team add ld_spucker
team modify ld_spucker color green
team modify ld_spucker nametagVisibility never
team add ld_kriecher
team modify ld_kriecher color aqua
team modify ld_kriecher nametagVisibility never
team add ld_platzer
team modify ld_platzer color gold
team modify ld_platzer nametagVisibility never
team add ld_brecher
team modify ld_brecher color red
team modify ld_brecher nametagVisibility never
team add ld_schreier
team modify ld_schreier color light_purple
team modify ld_schreier nametagVisibility never
bossbar add modpack:leader_laeufer {"text":"Läufer"}
bossbar set modpack:leader_laeufer name {"text":"Läufer","color":"yellow","bold":true}
bossbar set modpack:leader_laeufer color yellow
bossbar set modpack:leader_laeufer style notched_6
bossbar set modpack:leader_laeufer visible false
bossbar add modpack:leader_spucker {"text":"Spucker"}
bossbar set modpack:leader_spucker name {"text":"Spucker","color":"green","bold":true}
bossbar set modpack:leader_spucker color green
bossbar set modpack:leader_spucker style notched_6
bossbar set modpack:leader_spucker visible false
bossbar add modpack:leader_kriecher {"text":"Kriecher"}
bossbar set modpack:leader_kriecher name {"text":"Kriecher","color":"aqua","bold":true}
bossbar set modpack:leader_kriecher color blue
bossbar set modpack:leader_kriecher style notched_6
bossbar set modpack:leader_kriecher visible false
bossbar add modpack:leader_platzer {"text":"Platzer"}
bossbar set modpack:leader_platzer name {"text":"Platzer","color":"gold","bold":true}
bossbar set modpack:leader_platzer color pink
bossbar set modpack:leader_platzer style notched_6
bossbar set modpack:leader_platzer visible false
bossbar add modpack:leader_brecher {"text":"Brecher"}
bossbar set modpack:leader_brecher name {"text":"Brecher","color":"red","bold":true}
bossbar set modpack:leader_brecher color red
bossbar set modpack:leader_brecher style notched_6
bossbar set modpack:leader_brecher visible false
bossbar add modpack:leader_schreier {"text":"Schreier"}
bossbar set modpack:leader_schreier name {"text":"Schreier","color":"light_purple","bold":true}
bossbar set modpack:leader_schreier color purple
bossbar set modpack:leader_schreier style notched_6
bossbar set modpack:leader_schreier visible false
schedule function modpack:leader/loop 5t replace
