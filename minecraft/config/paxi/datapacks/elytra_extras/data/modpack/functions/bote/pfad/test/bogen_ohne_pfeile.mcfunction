# TEST: removes all your arrows and puts a Phoenix Bow (path item) in your hand
clear @s minecraft:arrow
clear @s minecraft:spectral_arrow
clear @s minecraft:tipped_arrow
item replace entity @s weapon.mainhand with aether:phoenix_bow{Unbreakable:1b,Enchantments:[{id:"minecraft:power",lvl:5s},{id:"minecraft:punch",lvl:2s},{id:"minecraft:infinity",lvl:1s}],display:{Lore:['{"text": "Gabe des Boten", "color": "gold", "italic": false}','{"text": "Pfad: Wissen", "color": "light_purple", "italic": false}']},modpack_questitem:1b,modpack_pfad:"wissen",modpack_teil:"waffe1"}
