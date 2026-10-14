# elytra_hordes (Paxi global datapack)

Roaming zombie hordes in the overworld, plus TaCZ gunfire noise for Zombie Awareness.
Loaded into every world by Paxi from `minecraft/config/paxi/datapacks/elytra_hordes/`.
Minecraft 1.20.1, pack_format 15. Function namespace `modpack`, scoreboards `mh_*`.

## Tuning: one file

All numbers are in **`data/modpack/functions/horde/settings.mcfunction`** (scoreboard constants
`#name` in objective `mh_cfg`). Edit, then `/reload`. To try a value without editing:
`/scoreboard players set #chance_pct mh_cfg 50` (reset on the next `/reload`).

| Setting | Default | Meaning |
|---|---|---|
| `#enabled` | 1 | hordes on/off |
| `#roll_every_s` | 60 | seconds of eligible play per roll (5 s steps) |
| `#chance_pct` | 15 | chance per roll, percent |
| `#cooldown_min` | 15 | minutes until the next horde; shared within 100 blocks |
| `#day_hordes` | 0 | 0 = night (13000-23000) or thunder only; 1 = also by day (zombies get unbreakable leather caps) |
| `#max_y` | 150 | no eligible time (and no lure) above this Y |
| `#skip_gliding` | 1 | no eligible time while gliding |
| `#size_min` / `#size_rand` | 8 / 4 | horde size 8-12 |
| `#mp_bonus` / `#mp_max_players` | 1 / 4 | +1 per extra player within 64 blocks, at most 4 |
| `#size_cap` | 16 | hard maximum per horde |
| `#armored` | 2 | first N zombies: iron helmet, chestplate, sword |
| `#weapon_pct` | 20 | others: % chance of stone sword / iron shovel / iron axe |
| `#dist_min` / `#dist_max` | 40 / 70 | spawn ring around the player (blocks) |
| `#max_hostiles` | 40 | skip if this many hostiles within 64 blocks |
| `#max_horde_total` | 48 | skip if this many horde zombies are loaded |
| `#lure_s` | 90 | seconds the horde is drawn to the player (renewed every 10 s) |
| `#lure_strength` | 150 | Zombie Awareness sense strength of the lure |
| `#despawn_s` | 180 | leftover age before removal (no player within 64, no target) |
| `#gunfire` | 1 | gunfire noise on/off |
| `#gun_strength` | 40 | gunfire sense strength (~26 blocks) |
| `#gun_cooldown_t` | 20 | ticks between gunfire senses per player |

Fixed in code (edit the function named): loop period 5 s (`horde/loop`), world-spawn exclusion
100 blocks and boss arena / rift gate exclusion 96 blocks (`horde/spot_check`), 128 blocks around
the player for arenas, 160 blocks "another horde nearby" (`horde/try_start`), hostile count radius
64 (`horde/try_start`), shared cooldown radius 100 (`horde/announce`), multiplayer count radius 64
(`horde/begin`), despawn player distance 64 (`horde/member_tick`), lure range check 128
(`horde/lure_tick`), 12 spot tries (`horde/begin`), underground limit 8 blocks below the surface
(`horde/try_start`), horde mix percentages (`horde/spawn_member`), structure list
(`predicates/horde/in_structure.json`), ground blocks (`tags/blocks/horde_ground.json`).

## How often

Defaults (night only): a Minecraft night gives about 8 minutes of eligible time = 8 rolls at 15 %,
so about 73 % of nights have a horde (at most one per night because of the 15 minute cooldown).
That is roughly one horde per 27 real minutes for a player who stays outside in the overworld at
night. Sleeping through nights skips them: set `#day_hordes 1` (about one per 22 minutes).

## What happens

1. Every 5 s each survival/adventure player in the overworld without cooldown collects eligible time
   (night or thunder, at or below `#max_y`, not gliding). Every `#roll_every_s` seconds: one roll.
2. A successful roll is cancelled if the player is more than 8 blocks under the surface, another
   horde is within 160 blocks, a boss arena or rift gate (elytra_dungeons markers `ed_arena`,
   `ed_rift_in`) is within 128 blocks, or a cap is reached.
3. Spot: random point 40-70 blocks away, dropped to the surface (leaves ignored), must be loaded, on
   natural ground (not water), with 2 free blocks, outside the listed structures, at least 100
   blocks from world spawn and 96 from any boss arena / rift gate. Up to 12 tries.
4. Spawn: 8-16 zombies by biome: normal 85 % zombie / 15 % zombie villager; desert/badlands 70 %
   husk; river/beach/swamp 40 % drowned. Tags `modpack_horde` (never `modpack_boss`/`ed_boss`),
   follow range 48, persistent until this pack removes them.
5. Warning: a quiet groan from the horde's direction and the actionbar text
   "You hear groaning in the distance" for players within 100 blocks.
6. Goal: a Zombie Awareness sound sense is placed at the player every 10 s for `#lure_s` seconds.
   Zombie Awareness then paths the horde there (zombies, husks, zombie villagers are in its
   `enhancedMobs`; drowned are not and rely on vanilla targeting, follow range 48).
7. Cleanup: horde zombies older than `#despawn_s` with no player within 64 blocks and no attack
   target are removed without drops.

Gunfire: TaCZ plays gun sounds through its own network packet, not a Minecraft sound event, so Zombie
Awareness never hears them. Every tick this pack looks for a new `tacz:bullet` within 8 blocks of a
player and puts a weak Zombie Awareness sound sense (strength 40, about 26 blocks) at the shooter.
Suppressed guns count the same (not detectable from a datapack).

## Commands

- `/function modpack:horde/start` force a horde near you (as a player)
- `/function modpack:horde/status` your cooldown, timer and nearby horde zombies
- `/scoreboard players get @s mh_cd` cooldown left in seconds; `/scoreboard players reset @s mh_cd` clears it
- `/function modpack:horde/clear` remove all loaded horde zombies (no drops) and this pack's senses
- `/kill @e[tag=modpack_horde]` also works (with drops)

## Notes

- The Zombie Awareness entity `zombieawareness:scent` and the TaCZ entity `tacz:bullet` are registered
  in code (no lang key), so `questtools/gamedata.py` does not list them. The pack refers to them through
  entity tags with `"required": false` (`tags/entity_types/za_senses.json`, `gun_bullets.json`), and the
  sense is summoned as a passenger with a single-quoted id. Both IDs were checked in the jars; see
  `questtools/hordecheck.py`.
- World spawn anchor: the load function puts a marker tagged `mh_spawn` at the world spawn (load
  functions run at the world spawn). Don't run `modpack:horde/load` by hand.
- Neat: zombie, husk, drowned and zombie villager are not in Neat's blacklist and horde zombies are on
  no team, so they show health bars like normal mobs.
