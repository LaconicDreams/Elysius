# as a player in a scene (every tick): sitting on their own seat? if not, back onto it
scoreboard players set #r mes_t 0
execute on vehicle if entity @s[tag=mes_seat] run scoreboard players set #r mes_t 1
execute if score #r mes_t matches 0 run function elytra_extras:messenger/scene/seat_mount
