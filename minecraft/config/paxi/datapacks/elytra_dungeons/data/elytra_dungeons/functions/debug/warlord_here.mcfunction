# test the Warlord fight anywhere: walk away 15+ blocks, then come back within 10
summon minecraft:marker ~ ~ ~ {Tags:["ed_arena","ed_warlord","ed_idle"]}
tellraw @s {"text":"Warlord arena marker placed here. Step within 10 blocks to start the fight.","color":"yellow"}
