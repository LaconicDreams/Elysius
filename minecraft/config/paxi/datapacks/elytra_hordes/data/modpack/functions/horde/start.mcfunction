# TEST: /function modpack:horde/start  (run as a player) forces a horde near you now.
# Ignores timer, chance, cooldown, time of day, altitude and caps; still needs a valid spot 40-70
# blocks away. Sets the shared cooldown like a normal horde.
tag @s[type=minecraft:player] add mh_force
execute if entity @s[type=minecraft:player] run function modpack:horde/begin
tag @s remove mh_force
