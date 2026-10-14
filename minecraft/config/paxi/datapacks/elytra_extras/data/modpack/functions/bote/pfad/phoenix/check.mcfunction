# as + at a Wissen player: obsidian pieces of the Wissen path become Phoenix again (NBT kept)
execute if entity @s[nbt={Inventory:[{Slot:103b,id:"aether:obsidian_helmet",tag:{modpack_pfad:"wissen"}}]}] run function modpack:bote/pfad/phoenix/slot_helm
execute if entity @s[nbt={Inventory:[{Slot:102b,id:"aether:obsidian_chestplate",tag:{modpack_pfad:"wissen"}}]}] run function modpack:bote/pfad/phoenix/slot_brust
execute if entity @s[nbt={Inventory:[{Slot:101b,id:"aether:obsidian_leggings",tag:{modpack_pfad:"wissen"}}]}] run function modpack:bote/pfad/phoenix/slot_hose
execute if entity @s[nbt={Inventory:[{Slot:100b,id:"aether:obsidian_boots",tag:{modpack_pfad:"wissen"}}]}] run function modpack:bote/pfad/phoenix/slot_stiefel
execute if entity @s[nbt={ForgeCaps:{"curios:inventory":{Curios:[{Identifier:"aether_gloves",StacksHandler:{Stacks:{Items:[{id:"aether:obsidian_gloves",tag:{modpack_pfad:"wissen"}}]}}}]}}}] run function #modpack:bote/pfad_handschuh
# not worn (in the inventory): replaced by a fresh Phoenix piece
execute store result score #n bote_pfeil run clear @s aether:obsidian_helmet{modpack_pfad:"wissen"}
execute if score #n bote_pfeil matches 1.. run function modpack:bote/pfad/item/wissen/helm
execute store result score #n bote_pfeil run clear @s aether:obsidian_chestplate{modpack_pfad:"wissen"}
execute if score #n bote_pfeil matches 1.. run function modpack:bote/pfad/item/wissen/brust
execute store result score #n bote_pfeil run clear @s aether:obsidian_leggings{modpack_pfad:"wissen"}
execute if score #n bote_pfeil matches 1.. run function modpack:bote/pfad/item/wissen/hose
execute store result score #n bote_pfeil run clear @s aether:obsidian_boots{modpack_pfad:"wissen"}
execute if score #n bote_pfeil matches 1.. run function modpack:bote/pfad/item/wissen/stiefel
execute store result score #n bote_pfeil run clear @s aether:obsidian_gloves{modpack_pfad:"wissen"}
execute if score #n bote_pfeil matches 1.. run function modpack:bote/pfad/item/wissen/handschuhe
