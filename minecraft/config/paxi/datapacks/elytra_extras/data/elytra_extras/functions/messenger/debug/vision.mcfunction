# TEST: jump to the vision: answers the deal with NEIN right now
function elytra_extras:messenger/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 4
scoreboard players set @s mes_answer 42
function elytra_extras:messenger/answer
