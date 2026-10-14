# TEST: shows Unbreakable and Damage of the item in your main hand (Unbreakable 1, Damage stays 0)
tellraw @s ["",{"text":"Unbreakable: "},{"nbt":"SelectedItem.tag.Unbreakable","entity":"@s"},{"text":"  Damage: "},{"nbt":"SelectedItem.tag.Damage","entity":"@s"},{"text":"  Pfad: "},{"nbt":"SelectedItem.tag.modpack_pfad","entity":"@s"}]
