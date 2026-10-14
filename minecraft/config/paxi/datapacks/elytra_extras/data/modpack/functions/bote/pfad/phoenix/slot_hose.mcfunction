data modify storage modpack:bote pfad.alt set from entity @s Inventory[{Slot:101b}].tag
item replace entity @s armor.legs with aether:phoenix_leggings
item modify entity @s armor.legs modpack:bote/pfad/nbt_zurueck
playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.6 1.4
