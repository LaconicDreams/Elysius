# as the player, at the swarm spot. AngryAt is copied from the player's own UUID (both are int arrays),
# so every bee hunts exactly this player
summon minecraft:bee ~0 ~ ~0 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
summon minecraft:bee ~1 ~ ~0 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
summon minecraft:bee ~0 ~ ~1 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
summon minecraft:bee ~-1 ~ ~0 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
summon minecraft:bee ~0 ~ ~-1 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
summon minecraft:bee ~1 ~ ~1 {Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,AngerTime:24000}
data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID
tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new
