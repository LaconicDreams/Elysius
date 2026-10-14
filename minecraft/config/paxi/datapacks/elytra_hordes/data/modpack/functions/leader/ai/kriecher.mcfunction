# Invisible in the dark, glowing and with an aura in light (light level >= 8 at its feet).
execute if predicate modpack:leader/lit run function modpack:leader/kriecher_lit
execute unless predicate modpack:leader/lit run effect give @s minecraft:invisibility 1 0 true
