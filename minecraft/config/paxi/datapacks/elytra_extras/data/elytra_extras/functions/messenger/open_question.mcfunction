# the scene's player (mes_cur) may answer
execute unless score #hidden mes_t matches 1 run function elytra_extras:messenger/feedback_off
tag @a[tag=mes_cur] add mes_asked
scoreboard players set @a[tag=mes_cur] mes_tm 120
scoreboard players enable @a[tag=mes_cur] mes_answer
