# as + at a macht player
execute unless entity @s[tag=gabe_waffe1] run function modpack:bote/pfad/gib/macht/waffe1
execute if score @s bote_rang matches 3.. unless entity @s[tag=gabe_helm] run function modpack:bote/pfad/gib/macht/helm
execute if score @s bote_rang matches 4.. unless entity @s[tag=gabe_brust] run function modpack:bote/pfad/gib/macht/brust
execute if score @s bote_rang matches 5.. unless entity @s[tag=gabe_hose] run function modpack:bote/pfad/gib/macht/hose
execute if score @s bote_rang matches 6.. unless entity @s[tag=gabe_stiefel] run function modpack:bote/pfad/gib/macht/stiefel
execute if score @s bote_rang matches 6.. unless entity @s[tag=gabe_handschuhe] run function modpack:bote/pfad/gib/macht/handschuhe
execute if score @s bote_rang matches 7.. unless entity @s[tag=gabe_waffe2] run function modpack:bote/pfad/gib/macht/waffe2
