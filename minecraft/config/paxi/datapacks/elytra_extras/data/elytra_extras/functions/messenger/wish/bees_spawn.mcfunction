# as + at the player: a swarm 10-15 blocks away on the surface, angry at this player
summon minecraft:marker ~ ~ ~ {Tags:["mes_rng"]}
execute store result score #r mes_t run data get entity @e[type=minecraft:marker,tag=mes_rng,limit=1,sort=nearest] UUID[0]
kill @e[type=minecraft:marker,tag=mes_rng]
execute if score #r mes_t matches ..-1 run scoreboard players operation #r mes_t *= #neg mes_t
scoreboard players operation #d mes_t = #r mes_t
scoreboard players operation #d mes_t %= #6 mes_t
scoreboard players operation #a mes_t = #r mes_t
scoreboard players operation #a mes_t /= #6 mes_t
scoreboard players operation #a mes_t %= #8 mes_t
execute if score #d mes_t matches 0 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 0 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 1 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^11 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 2 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 3 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 4 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 0 rotated 0 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 1 rotated 45 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 2 rotated 90 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 3 rotated 135 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 4 rotated 180 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 5 rotated 225 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 6 rotated 270 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
execute if score #d mes_t matches 5 if score #a mes_t matches 7 rotated 315 0 positioned ^ ^ ^15 positioned over motion_blocking_no_leaves positioned ~ ~2 ~ run function elytra_extras:messenger/wish/bees_here
playsound minecraft:entity.bee.loop_aggressive hostile @s ~ ~ ~ 1 0.8
