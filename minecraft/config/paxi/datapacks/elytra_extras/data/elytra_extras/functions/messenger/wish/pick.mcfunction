# as + at a player who clicked a wish (once per player). mes_wish: 1 Macht, 2 Schutz, 3 Wissen
tag @s add mes_has_wish
scoreboard players operation @s mes_wish = @s mes_answer
scoreboard players remove @s mes_wish 50
scoreboard players set @s mes_pflag 0
scoreboard players set @s mes_hp 0
execute if score @s mes_wish matches 1 run function elytra_extras:messenger/wish/macht
execute if score @s mes_wish matches 2 run function elytra_extras:messenger/wish/schutz
execute if score @s mes_wish matches 3 run function elytra_extras:messenger/wish/wissen
# HOOK: later wishes (mes_wish 4, 5, ...) are dispatched here
# HOOK: everything that comes with the chosen path (path rewards) listens to this function tag
function #modpack:bote/wunsch_gewaehlt
# chosen without a scene (test function): the price starts at once
execute unless entity @s[tag=mes_scene] run function elytra_extras:messenger/wish/start_price
tellraw @a[tag=mes_cur] ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr werdet von mir hören.", "color": "#FFE9A8", "italic": true, "bold": false}]
execute at @s run playsound minecraft:entity.wandering_trader.ambient neutral @a[tag=mes_cur] ~ ~ ~ 1 0.7
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid run function elytra_extras:messenger/wish/leave_soon
