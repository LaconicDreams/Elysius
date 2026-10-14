# four end crystals on the pillars (positions are relative to the altar marker)
summon minecraft:end_crystal ~-10 ~5 ~-10 {Tags:["ed_magus_crystal"],ShowBottom:0b,BeamTarget:{X:0,Y:88,Z:0}}
summon minecraft:end_crystal ~10 ~5 ~-10 {Tags:["ed_magus_crystal"],ShowBottom:0b,BeamTarget:{X:0,Y:88,Z:0}}
summon minecraft:end_crystal ~-10 ~5 ~10 {Tags:["ed_magus_crystal"],ShowBottom:0b,BeamTarget:{X:0,Y:88,Z:0}}
summon minecraft:end_crystal ~10 ~5 ~10 {Tags:["ed_magus_crystal"],ShowBottom:0b,BeamTarget:{X:0,Y:88,Z:0}}
playsound minecraft:block.beacon.activate hostile @a[distance=..64] ~ ~ ~ 2 0.8
