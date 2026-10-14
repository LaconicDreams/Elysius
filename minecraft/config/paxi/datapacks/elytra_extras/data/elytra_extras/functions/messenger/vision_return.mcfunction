# as the player in the vision who answered JA: back to where they stood (still frozen), the deal is accepted
function elytra_extras:messenger/vision_back
function elytra_extras:messenger/tag_mine
execute at @s facing entity @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={mes_stage=4},limit=1] at @s run function elytra_extras:messenger/accept_deal
