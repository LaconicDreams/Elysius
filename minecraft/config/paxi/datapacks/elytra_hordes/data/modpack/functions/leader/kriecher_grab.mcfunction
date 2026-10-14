# Advancement reward, as a player the Kriecher just hit: legs grabbed.
effect give @s minecraft:slowness 3 2 true
playsound minecraft:entity.spider.ambient hostile @s ~ ~ ~ 1 0.5
title @s actionbar {"text":"Something grabs your legs!","color":"aqua"}
advancement revoke @s only modpack:leaders/kriecher_grab
