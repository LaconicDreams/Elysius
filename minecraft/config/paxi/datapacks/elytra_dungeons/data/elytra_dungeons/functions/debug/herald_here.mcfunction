# test the Tempest Herald anywhere (best high up in the open): walk 15+ blocks away, then come back within 14
summon minecraft:marker ~ ~ ~ {Tags:["ed_arena","ed_spire","ed_idle"]}
tellraw @s {"text":"Herald arena marker placed here. Come within 14 blocks to start the fight.","color":"yellow"}
