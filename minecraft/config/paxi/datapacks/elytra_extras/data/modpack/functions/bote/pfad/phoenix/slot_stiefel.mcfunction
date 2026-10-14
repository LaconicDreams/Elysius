data modify storage modpack:bote pfad.alt set from entity @s Inventory[{Slot:100b}].tag
item replace entity @s armor.feet with aether:phoenix_boots
item modify entity @s armor.feet modpack:bote/pfad/nbt_zurueck
playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.6 1.4
