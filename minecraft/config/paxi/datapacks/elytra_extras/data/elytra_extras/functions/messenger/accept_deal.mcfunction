# as + at the Bote: deal accepted -> his player gets the wish question if they have none; else the shop opens
function elytra_extras:messenger/tag_owner
scoreboard players set @s mes_stage 5
# the pact is made (the rank system gives its points for this advancement)
advancement grant @a[tag=mes_cur] only elytra_extras:bote/pakt
execute store result score #nw mes_t if entity @a[tag=mes_cur,tag=!mes_has_wish]
execute if score #nw mes_t matches 0 run function elytra_extras:messenger/open_shop
execute if score #nw mes_t matches 1.. run function elytra_extras:messenger/wish/ask
