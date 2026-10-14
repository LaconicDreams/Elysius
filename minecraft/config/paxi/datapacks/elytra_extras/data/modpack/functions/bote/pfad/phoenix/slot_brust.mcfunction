data modify storage modpack:bote pfad.alt set from entity @s Inventory[{Slot:102b}].tag
item replace entity @s armor.chest with aether:phoenix_chestplate
item modify entity @s armor.chest modpack:bote/pfad/nbt_zurueck
playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.6 1.4
