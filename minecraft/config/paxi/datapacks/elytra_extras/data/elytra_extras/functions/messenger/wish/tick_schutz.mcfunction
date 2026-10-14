# milk or death removed the effect: give it back while the price lasts
execute if score @s mes_ptime matches 1.. unless predicate elytra_extras:messenger/has_fatigue run effect give @s minecraft:mining_fatigue infinite 0 true
execute if score @s mes_ptime matches ..0 run function elytra_extras:messenger/wish/schutz_done
