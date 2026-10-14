# Rangsystem: scoreboards, teams, loop
scoreboard objectives add bote_punkte dummy
scoreboard objectives add bote_rang dummy
scoreboard objectives add bote_ziel dummy
scoreboard objectives add bote_rwait dummy
scoreboard objectives add bote_rkt minecraft.used:minecraft.firework_rocket
scoreboard objectives add bote_rkn dummy
scoreboard objectives add bote_snk minecraft.custom:minecraft.sneak_time
scoreboard objectives add bote_snc dummy
scoreboard objectives add bote_cd6 dummy
scoreboard objectives add bote_cd7 dummy
scoreboard objectives add bote_hp health
scoreboard objectives add bote_anr dummy
scoreboard players set #20 bote_rang 20
team add rang_1
team modify rang_1 prefix {"text": "[Sandkorn] ", "color": "gray"}
team modify rang_1 color gray
team modify rang_1 friendlyFire true
team modify rang_1 nametagVisibility always
team add rang_2
team modify rang_2 prefix {"text": "[Minutenzeiger] ", "color": "white"}
team modify rang_2 color white
team modify rang_2 friendlyFire true
team modify rang_2 nametagVisibility always
team add rang_3
team modify rang_3 prefix {"text": "[Stundengänger] ", "color": "yellow"}
team modify rang_3 color yellow
team modify rang_3 friendlyFire true
team modify rang_3 nametagVisibility always
team add rang_4
team modify rang_4 prefix {"text": "[Tagwandler] ", "color": "green"}
team modify rang_4 color green
team modify rang_4 friendlyFire true
team modify rang_4 nametagVisibility always
team add rang_5
team modify rang_5 prefix {"text": "[Siegelträger] ", "color": "aqua"}
team modify rang_5 color aqua
team modify rang_5 friendlyFire true
team modify rang_5 nametagVisibility always
team add rang_6
team modify rang_6 prefix {"text": "[Zeitenwandler] ", "color": "light_purple"}
team modify rang_6 color light_purple
team modify rang_6 friendlyFire true
team modify rang_6 nametagVisibility always
team add rang_7
team modify rang_7 prefix {"text": "[Gefährte des Boten] ", "color": "gold"}
team modify rang_7 color gold
team modify rang_7 friendlyFire true
team modify rang_7 nametagVisibility always
# the old manual friendly-fire team: players now sit in the rank teams (friendly fire on there)
team remove friends
schedule function modpack:bote/rang/loop 10t replace
