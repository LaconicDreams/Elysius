tag @s add mes_mus_on
scoreboard players remove @s mes_mus 10
execute if score @s mes_mus matches ..0 run function elytra_extras:messenger/scene/music_play
