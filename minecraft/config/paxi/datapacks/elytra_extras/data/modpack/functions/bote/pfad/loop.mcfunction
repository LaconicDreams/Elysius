# every 10 ticks
schedule function modpack:bote/pfad/loop 10t replace
# what each player is owed (catch-up included; nothing twice). Not during a Bote scene
execute as @a[tag=!mes_scene,scores={mes_wish=1..3}] at @s run function modpack:bote/pfad/pruefen
# Phoenix armour turned to Obsidian by water: back to Phoenix
execute as @a[scores={mes_wish=3}] at @s run function modpack:bote/pfad/phoenix/check
# Phoenix Bow helper arrow: only while the bow is held; never on the ground
execute as @a unless predicate modpack:bote/pfad/bogen_in_hand run clear @s minecraft:arrow{modpack_bogenpfeil:1b}
kill @e[type=minecraft:item,nbt={Item:{tag:{modpack_bogenpfeil:1b}}}]
# lost items: /trigger bote_gabe
scoreboard players enable @a[scores={mes_wish=1..3}] bote_gabe
scoreboard players remove @a[scores={bote_gcd=1..}] bote_gcd 10
execute as @a[scores={bote_gabe=1..}] at @s run function modpack:bote/pfad/verlust/anfrage
