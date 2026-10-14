# TEST: jump to the lie: answers question 1 with NEIN right now (damage, red eyes, music stops)
function elytra_extras:messenger/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 1
scoreboard players set @s mes_answer 12
function elytra_extras:messenger/answer
