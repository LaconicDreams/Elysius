# =====================================================================================
#  ZOMBIE HORDE SETTINGS  (the only file you need to edit; then run /reload)
#  Every number is a scoreboard constant: fake player "#name" in objective mh_cfg.
#  Look at one in game:      /scoreboard players get #chance_pct mh_cfg
#  Try one without editing:  /scoreboard players set #chance_pct mh_cfg 50   (reset by /reload)
# =====================================================================================

# --- on/off ---------------------------------------------------------------------------
# 1 = roaming hordes on, 0 = off (gunfire noise has its own switch, #gunfire)
scoreboard players set #enabled mh_cfg 1

# --- how often --------------------------------------------------------------------------
# A player collects "eligible time" while in the overworld, in survival/adventure, at or below #max_y,
# not gliding, and (unless #day_hordes is 1) at night or in a thunderstorm. Each time it reaches
# #roll_every_s seconds the player rolls #chance_pct percent. The timer counts in 5 second steps.
scoreboard players set #roll_every_s mh_cfg 60
scoreboard players set #chance_pct mh_cfg 15
# Minutes before the next horde after one started. Shared by every player within 100 blocks of the
# player who got the horde, so friends are not hit by overlapping hordes.
scoreboard players set #cooldown_min mh_cfg 15
# 0 = hordes only at night (time 13000-23000) or in thunderstorms, when zombies don't burn.
# 1 = also by day; every horde zombie then gets an unbreakable leather cap so it does not burn.
scoreboard players set #day_hordes mh_cfg 0

# --- elytra ------------------------------------------------------------------------------
# No eligible time while the player is above this Y (feet), and the lure stops above it too
scoreboard players set #max_y mh_cfg 150
# 1 = no eligible time while gliding with an elytra at any height
scoreboard players set #skip_gliding mh_cfg 1

# --- size ----------------------------------------------------------------------------------
# size = #size_min + random(0..#size_rand) + #mp_bonus per extra player within 64 blocks
#        (at most #mp_max_players extra players count), never more than #size_cap
scoreboard players set #size_min mh_cfg 8
scoreboard players set #size_rand mh_cfg 4
scoreboard players set #mp_bonus mh_cfg 1
scoreboard players set #mp_max_players mh_cfg 4
scoreboard players set #size_cap mh_cfg 16
# The first #armored zombies get an iron helmet, iron chestplate and iron sword.
# Every other one has #weapon_pct percent chance of a stone sword, iron shovel or iron axe.
scoreboard players set #armored mh_cfg 2
scoreboard players set #weapon_pct mh_cfg 20

# --- where -----------------------------------------------------------------------------------
# Spawn distance from the player, in blocks (a ring). Keep #dist_max at 70 or less: with simulation
# distance 6 chunks further out may not be loaded. Fixed in code: never within 100 blocks of world
# spawn, never within 96 blocks of a boss arena or rift gate, never inside villages/outposts/temples/
# dungeon structures, only on natural ground (dirt, grass, sand, stone, snow, gravel...), never on water.
scoreboard players set #dist_min mh_cfg 40
scoreboard players set #dist_max mh_cfg 70

# --- safety caps -----------------------------------------------------------------------------
# No horde if this many hostile mobs are already within 64 blocks of the player
scoreboard players set #max_hostiles mh_cfg 40
# No new horde while this many horde zombies are alive in loaded chunks (all players together)
scoreboard players set #max_horde_total mh_cfg 48

# --- behaviour -------------------------------------------------------------------------------
# For this many seconds after the start, a Zombie Awareness sound sense is put at the target player's
# position every 10 seconds, so the horde walks towards them (stops above #max_y or if no horde zombie
# is within 128 blocks). Use a multiple of 10.
scoreboard players set #lure_s mh_cfg 90
# Strength of that sense. Zombie Awareness range = strength / 100 * maxPFRangeSense (64), fading over
# 30 s; mobs only search 64 blocks (maxPFRangeSense) anyway.
scoreboard players set #lure_strength mh_cfg 150
# Leftover horde zombies are removed after this many seconds if no player is within 64 blocks and
# they have no target.
scoreboard players set #despawn_s mh_cfg 180

# --- gunfire (TaCZ) --------------------------------------------------------------------------
# TaCZ gunshots are not sound events Zombie Awareness can hear, so this pack adds a Zombie Awareness
# sound sense at a player who fires (bullet entity seen next to them). 1 = on, 0 = off.
scoreboard players set #gunfire mh_cfg 1
# Strength 40 -> about 26 blocks (block-breaking noise is ~58, explosions 64 = the search cap)
scoreboard players set #gun_strength mh_cfg 40
# At most one new/refreshed gunfire sense per player every this many ticks (20 = 1 s)
scoreboard players set #gun_cooldown_t mh_cfg 20
