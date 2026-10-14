# TEST: jump to the wish choice: answers the deal with JA right now (debug/wish_reset first if you have a wish)
function elytra_extras:messenger/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 4
scoreboard players set @s mes_answer 41
function elytra_extras:messenger/answer
