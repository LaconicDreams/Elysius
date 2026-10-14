# Elytra modpack changelog

Paths are relative to the Prism instance folder (`%APPDATA%\PrismLauncher\instances\1.20.1`).

## Boss dungeons task

### Phase 1: worldgen cleanup (2026-10-08)
No game files were changed. Only reports were added:
- added `devnotes/phase1_worldgen_report.md`: structures per mod, overlaps, removal proposal, dependency check
- added `devnotes/chunky_pregen_commands.md`: Chunky pregeneration plan for the overworld, Nether, Aether and End
- added `CHANGELOG.md` (this file)
- added `PROJECT_SUMMARY.md`: updated project summary

Decisions (approved): keep Repurposed Structures but trim it with a datapack, remove Cloth Config, add Paxi (global datapacks) and Chunky.

Then changed:
- **moved** `minecraft/mods/cloth-config-11.1.136-forge.jar` to `backup/2026-10-08_233121_phase1/mods/` (nothing depended on it)
- **added** `minecraft/mods/Paxi-1.20-Forge-4.0.jar` (Modrinth, SHA-1 a3a7008e07a27b3c831af7e4c82fbbc10a4da328; needs YUNG's API, installed)
- **added** `minecraft/mods/Chunky-1.3.146.jar` (Modrinth, SHA-1 0b782d12b4ac3b03a94c28f32e9b2d5587d1dd50)
- **added** `minecraft/config/paxi/datapacks/elytra_rs_trim/`: pack_format 15. It replaces 34 Repurposed Structures biome tags with empty lists, so these only stop generating in **new** chunks:
  - mineshafts: birch, dark_forest, desert, icy, jungle, ocean, savanna, stone, swamp, taiga
  - pyramids: badlands, dark_forest, flower_forest, giant_tree_taiga, icy, jungle, mushroom, ocean, snowy
  - monuments: desert, icy, jungle
  - temples: ocean, taiga
  - dungeon features: badlands, dark_forest, deep, desert, icy, jungle, mushroom, ocean, snow, swamp

  Kept: all Repurposed Structures Nether and End content, villages, outposts, igloos, witch huts, ruins, shipwrecks, mansions, cities, wells.
- **changed** `questtools/validate.py`: now also checks Paxi datapacks (pack.mcmeta, JSON syntax, overrides that match no installed mod file)
- `check-mods.ps1` rerun with 49 jars: no missing dependencies or version mismatches

### Phase 2: first boss dungeon, Ashen Barrow (2026-10-09)
- **added** `minecraft/config/paxi/datapacks/elytra_dungeons/` (38 files): structure NBT pieces (entrance, corridor_a,
  corridor_b, arena), template pools, decay processor list, structure + structure set, biome tag, 6 loot tables,
  17 functions (load, loop, fight logic, debug), 2 advancements, `minecraft:load` function tag
- **added** `questtools/dungeongen.py`: builds the pack and backs up the old pack to `backup/<time>_elytra_dungeons` first
- **added** `questtools/structlib.py` (structure/datapack building, block-state checks), `questtools/nbt.py`
  (binary NBT read/write), `questtools/packcheck.py` (deep datapack checks)
- **changed** `questtools/gamedata.py`: indexes blocks, biomes, biome tags, loot tables, trims, particles, sounds
  (vanilla sounds from the launcher asset index), effects and enchantments
- **changed** `questtools/validate.py`: runs the deep datapack checks before launch (tested: catches a broken jigsaw
  link, unknown loot item, unknown entity, missing function)
- **added** `devnotes/phase2_ashen_barrow.md`: design, fight table and test commands
- **changed** (2026-10-09, barrows spawned ~58k blocks out): the start piece is now a surface `ruin`, joined by a
  vertical jigsaw to a new `shaft` piece, so the biome is checked at ground level instead of 20 blocks underground.
  Spacing 32/16 -> 24/8. 8 more Terralith biomes (arid_highlands, fractured_savanna, savanna_slopes,
  sandstone_valley, desert_spires, scarlet_mountains, warped_mesa, gravel_desert). The shaft lantern was moved off
  the landing pool's drop line. The old `entrance` template is kept for barrows that already generated.
  Previous pack in `backup/2026-10-09_002149_elytra_dungeons`.
- **added** function `elytra_dungeons:debug/rearm` (restart the fight of arenas within 64 blocks); previous pack in
  `backup/2026-10-09_001517_elytra_dungeons`

### Phase 3: Storm Spire, Rift Gates, the Hollow (2026-10-09)
- **changed** `minecraft/config/paxi/datapacks/elytra_dungeons/` (now 120 files; previous version in
  `backup/2026-10-09_003859_elytra_dungeons`):
  - Storm Spire: structure, set, biome tag, piece `storm_spire/spire`, 15 functions, tower/reward/boss loot,
    advancement `bosses/tempest_herald`
  - Rift Gate: structure, set, biome tag, piece `hollow/gate`
  - The Hollow: `dimension/the_hollow`, `dimension_type/the_hollow`, `worldgen/biome/hollow`, arena piece
    `hollow/arena`, travel and fight functions, loot, advancement `bosses/hollow_magus`
  - shared: new scoreboards (ed_wave, ed_shield, ed_tmp, ed_const, ed_flag, ed_pid, ed_cd, ed_deaths), 3 boss bars,
    loop calls, debug functions herald_here / hollow_enter / hollow_rebuild, rearm and clear_markers cover all bosses
- **added** `questtools/dungeons_p3.py`
- **changed** `questtools/dungeongen.py` (wires in Phase 3), `questtools/structlib.py` (vertical jigsaws),
  `questtools/packcheck.py` (dimensions, dimension types, biomes, `execute in`, `place template`; tested with
  3 planted errors)
- **added** `devnotes/phase3_sky_and_hollow.md`

#### Phase 3 fixes after the first test (2026-10-09)
Reported: the core was inside the ghast and couldn't be hit, no lightning in phase 2, the ghast was stuck in a
corner and not attacking, the platform was too small, the design needed changing.
- Storm Spire redesigned as the **Tempest Crown**: new piece `storm_spire/crown` (47x17x47, 39-wide arena,
  rim with 4 openings, 8 edge columns, south dock with the resupply barrel, vault under a trapdoor). The old
  `storm_spire/spire` piece is kept for spires that already generated.
- Herald now has NoAI with **scripted orbit** (radius 10, +11 height, faces the nearest player) and **scripted
  aimed fireballs** (every 3 s, 2 s in phase 2). He stays over the platform, so drops land on it.
- Storm Core no longer rides the ghast: a medium slime kept 4.5 blocks above his head every tick.
- Lightning: targets any non-spectator player (it skipped creative players before), with a 1 s spark warning
  before each strike.
- New `elytra_dungeons:tick` function (`minecraft:tick` tag), only active during a Herald fight; scoreboards
  `ed_angle`, `ed_fb`.
- Previous pack in `backup/2026-10-09_005047_elytra_dungeons`.

#### Hollow Magus: reskin and size (2026-10-09)
Reported: no reskin, too small for the arena (keep the chamber as it is).
- **added** `minecraft/mods/Pehkui-3.8.2+1.20.1-forge.jar` (Modrinth, SHA-1 4bc816efdd8e5e2a97423313674401351710e403),
  the only way to resize a mob on 1.20.1; dependency check still clean
- Magus is now an **illusioner** (never spawns naturally, so its texture can be changed without affecting
  anything else). Scaled to **2x** with `scale set pehkui:base 2` and `pehkui:motion 0.6`. Power II bow.
  Scripted **evoker-fang lines** at the nearest player every 4 s. Shield, waves, pulse, loot and arena unchanged.
- **added** `minecraft/config/paxi/resourcepacks/elytra_dungeons_rp/`: void-purple illusioner texture, generated
  from the vanilla texture by `questtools/pngtool.py`
- **changed** `questtools/dungeongen.py` (writes the resource pack too, with backups), `questtools/validate.py`
  (checks resource packs: pack_format and that each texture replaces a real vanilla texture of the same size),
  `questtools/packcheck.py` (Pehkui must be installed if `/scale` is used)
- Previous datapack in `backup/2026-10-09_005832_elytra_dungeons`

#### Tempest Herald: reskin, ruby weak point, rocket barrel (2026-10-09)
Reported: the Herald needs a reskin; the core couldn't be hit because the facing ghast blocked it; wanted a gem on
the forehead; the rocket barrel should give 4 stacks.
- Herald body is now a **custom ghast-shaped model** (item_display of paper with CustomModelData 7101; normal
  paper is unchanged). The real ghast is invisible and only serves as the hitbox. Storm texture made from the
  vanilla ghast texture: slate body, glowing cyan eyes, mouth and underside, ruby on the forehead. Face and ruby
  on front and back. The model turns left/right with the Herald but never tilts.
- Weak point: an invisible **Storm Ruby** hitbox (medium slime) kept on the painted ruby, 0.35 blocks in front of
  the face, marked with red sparkles. Still x3 damage to the Herald.
- Rocket barrel now refills with **4 stacks (256 rockets)** when it has none left (60 s cooldown).
- Resource pack: added `assets/elytra_dungeons/models/item/tempest_herald.json`,
  `assets/elytra_dungeons/textures/entity/tempest_herald.png`, `assets/minecraft/models/item/paper.json`
  (override only). Previous versions in `backup/2026-10-09_010707_elytra_dungeons` and
  `backup/2026-10-09_010708_elytra_dungeons_rp`.

#### Fixes from the second Herald test (2026-10-09)
Reported: the Herald was all black; 3 slime "cores" stood still in the arena, visible, with health bars.
Found in `logs/latest.log`: missing texture `elytra_dungeons:entity/tempest_herald` in model `minecraft:paper`, and
`Failed to load function elytra_dungeons:ashen_barrow/fire_nova` ("Only one entity is allowed").
- Herald texture moved to `assets/elytra_dungeons/textures/item/tempest_herald.png` (item models can only use
  textures under textures/block or textures/item); the model now refers to `elytra_dungeons:item/tempest_herald`.
- Storm Ruby: 1000 HP, refilled **every tick** (it ran every 5 ticks), so it can never die. Medium slimes split into
  small slimes when they die; those untagged leftovers were the stuck "cores". Before any ruby is removed it is
  shrunk to Size 0 (which doesn't split).
- Warlord `fire_nova`: `damage` accepts one target only, so it now loops over the players with `execute as`. Phase 3
  fire bursts never worked before this fix.
- Validator: errors on single-target commands given a multi-entity selector (damage, data ... entity,
  store ... entity, ride, facing entity, damage ... by), and on model textures outside block/ or item/ (or missing).
  Both checks were tested on the broken pack and caught all three errors.
- Previous versions in `backup/2026-10-09_011549_elytra_dungeons` and `backup/2026-10-09_011550_elytra_dungeons_rp`.

## Earlier work (same day, before this task)
- `check-mods.ps1`: mod dependency/version checker
- `questtools/`: quest generator (`questgen.py`, `questlib.py`), validator (`validate.py`), balance auditor (`balance.py`), loot generator (`lootgen.py`), shared code (`snbt.py`, `gamedata.py`), ID store (`ids.json`), backups in `questtools/backups/`
- `instance.cfg`: pre-launch command runs `questtools/validate.py` (original saved as `questtools/backups/instance.cfg.bak`)
- `minecraft/config/ftbquests/quests/chapters/*.snbt`: regenerated from `questgen.py`. Changes: ammo prices (bulk = one stack), stack splitting, no popups in shop chapters, Sky's the Limit reward is now an unbreakable netherite chestplate, corrected descriptions. Every earlier version is in `questtools/backups/<timestamp>/`.
- `minecraft/tacz/elytra_loot/`: TaCZ gun pack that adds guns, attachments and ammo to 291 structure chest loot tables (5 tiers)

## Jade + Neat (health display)
2026-10-09. Backup of mods/ and config/ before the change: `backup/2026-10-09_010902_jade_neat/`.
No overlapping HUD/health mods were installed (no WTHIT, HWYLA, The One Probe, ToroHealth or other health bars).
- **added** `minecraft/mods/Jade-1.20.1-Forge-11.13.3.jar` (Modrinth, 553487 bytes,
  SHA-1 d08e64e66521d69e083c8525f1fc507f1c202384). mods.toml: javafml, needs only forge [46,).
- **added** `minecraft/mods/Neat-1.20.1-41-FORGE.jar` (Modrinth, 30595 bytes,
  SHA-1 32fe1c807ac0c6aed8045260934f1ba6dc491361). mods.toml: javafml, needs only forge [45.0.40,).
- **added** `questtools/configure_hud.py`: applies the Neat settings below (keys read from the Neat jar), keeps
  comments, backs up the old file, re-parses with tomllib, checks the entity IDs with gamedata. Safe to re-run.
- **changed** `minecraft/config/neat-client.toml` [general] (by configure_hud.py; old file in
  `backup/2026-10-09_011607_configure_hud/`):
  max_distance_without_line_of_sight 8 -> 0, show_entity_full_health true -> false, display_on_players true -> false,
  display_on_bosses true -> false, show_on_passive true -> false, health_bar_height 4 -> 3, background_height 6 -> 5,
  hp_text_height 14 -> 10, show_max_hp true -> false, show_hp_percentage true -> false, show_attributes true -> false,
  show_armor true -> false; blacklist: the 7 defaults kept + alexsmobs:void_worm, alexsmobs:void_worm_part,
  minecraft:illusioner, minecraft:bat, alexsmobs:fly, alexsmobs:cockroach, alexsmobs:crimson_mosquito,
  alexsmobs:anaconda_part, alexsmobs:bone_serpent_part, alexsmobs:centipede_body, alexsmobs:centipede_tail.
  (max_distance stays 24 = default.)
- Jade: `minecraft/config/jade/*.json` unchanged (defaults already fit: top centre, under boss bars, health shown,
  registry name off).

How Neat decides (from the jar, `HealthBarRenderer.shouldShowPlate`), for future bosses:
- Living entities only. Skipped when: type ID is in `blacklist` (exact IDs, no tags); farther than max_distance;
  no line of sight; `display_on_bosses = false` and the type is in `#forge:bosses` or `#c:bosses`; the mob is
  invisible to you and wears/holds nothing; its scoreboard team has nametagVisibility never (or hides it for your team).
- `#forge:bosses` covers minecraft:ender_dragon, minecraft:wither (Forge) and aether:slider, aether:valkyrie_queen,
  aether:sun_spirit (Aether jar). Alex's Mobs has no boss tag, so its void worm is blacklisted by ID.
- Pack bosses are vanilla types, so a type ID can't single them out. Tempest Herald (invisible ghast) and the Storm
  Ruby (invisible slime) are already skipped because they are invisible and hold nothing. The Hollow Magus is
  hidden by the minecraft:illusioner blacklist entry. The Ashen Warlord (wither skeleton with gear) still gets a
  bar. **Every new boss must be excluded from Neat**: either use a type that never appears naturally and blacklist
  it, or put the boss on a scoreboard team with `nametagVisibility never` (this also hides its name tag; the boss
  bar still shows the name).

#### Boss team for Neat (main session, 2026-10-09)
- `elytra_dungeons` datapack: `load` creates team `ed_bosses` with `nametagVisibility never`. Every 5 ticks, `loop`
  adds every entity tagged `ed_boss` (all bosses) and `ed_herald_core` (Storm Ruby) to it. Neat skips entities
  whose team hides nametags, so the Ashen Warlord (a wither skeleton, which can't be blacklisted by type) no
  longer gets a Neat bar. Normal wither skeletons are unaffected. Floating boss names are hidden; the boss bar
  shows the name.
- **Rule for future bosses:** give them the scoreboard tag `ed_boss` when summoning, and they are excluded
  automatically.
- Previous pack in `backup/2026-10-09_011737_elytra_dungeons`.

#### Reward chest fix (main session, 2026-10-09)
Reported: in the Hollow the boss spawned on top of the reward chest, and the chest was empty.
Cause: the reward chest was placed on the Magus's spawn spot. After a re-arm, `setblock` found the identical
chest already there, did nothing, and the old, already-looted chest stayed.
- All three bosses (`ashen_barrow/victory`, `storm_spire/victory`, `hollow/victory`): an empty leftover chest is
  replaced with a fresh one. If the old chest still holds items it is kept and the new reward is dropped on top
  of it instead (`loot spawn`), so nothing is lost.
- Hollow: the reward chest is now 2 blocks south of the altar centre (still on the altar). `hollow/start` breaks
  any chest on the spawn spot first (`setblock ... air destroy`, so its contents drop); this clears the one already
  in existing worlds.
- Previous versions in `backup/2026-10-09_013625_elytra_dungeons`.

## Zombie hordes (Zombie Awareness + elytra_hordes datapack)
2026-10-09. Backup of `minecraft/config/` (incl. all Paxi packs) before any change:
`backup/zombie-2026-10-09_012900/`. World datapack folders were empty (nothing to back up).

Findings (from the Zombie Awareness 1.13.1 and TaCZ jars):
- Zombie Awareness has no horde **spawning**. `wanderingHordes` only drops a random "waypoint" sense
  within 64 blocks of each player every N seconds, and idle mobs nearby walk to it in loose groups.
  Its `ZAConfigSpawning` (extra spawns) and `SoundLists` classes exist in the jar but are never
  registered in 1.13.1, so there are no spawn-rate keys and no configurable sound list. The sounds
  it reacts to are hard-coded (doors, note blocks, levers, buttons, plates, tripwire, barrels,
  block placing, burps, zombie groans, pistons, explosions) plus block breaking/hitting.
- TaCZ gunshots are not sound events: `SoundManager.sendSoundToNearby` sends its own network packet
  (`ServerMessageSound`) straight to players, so Zombie Awareness can never hear them. The datapack
  adds gunfire noise itself (below).
- `zombieRandSpeedBoost` applies to every naturally spawned zombie (up to +30 % speed), not only
  "extra spawns" as its comment says. Left at 0.3.

Changed `minecraft/config/zombieawareness/General.toml`:
- `sightRange` 16 -> 24 (moderate extra sight, line of sight still needed)
- `soundStrength` 60 -> 70 (block noise reaches ~58 blocks instead of ~50; search is capped by
  `maxPFRangeSense` 64, unchanged)
- `findSense_PercentChance` 10 -> 20 (zombies pick up sounds/scents/lures sooner)
- `tickRateAILoop` 5 -> 10 (performance: half as many awareness AI passes)
- `blockBreakEvent_PlayersOnly` false -> true (performance: only players' block breaking makes noise)

Changed `minecraft/config/zombieawareness/Features.toml`:
- `wanderingHordes` false -> true (native roaming groups of existing mobs)
- `frequencyOfWanderingHordesPerPlayer` 30 -> 120 (seconds; less pathfinding than the default)

Unchanged on purpose: scent on (`awareness_Scent`, `scentStrength` 60), sound on, `omniscient` and
`seeThroughWalls` false, light awareness zombies-only, `tickCooldownBetweenPathfinds` 300, CoroUtil
`General.toml` (logging only, no performance keys). Zombie Awareness has no zombie block-breaking and
no daylight-burning option (vanilla behaviour stays). Neat/Jade: no change needed (zombie, husk,
drowned, zombie villager are not blacklisted in `neat-client.toml` or `jade/hide-entities.json`).

Added `minecraft/config/paxi/datapacks/elytra_hordes/` (Paxi global datapack, pack_format 15):
- `README.md`: settings table, frequency math, commands, notes
- `data/modpack/functions/horde/` (23 functions): `settings` (all tunables, objective `mh_cfg`),
  `load`, `loop` (every 5 s), `player_tick`, `roll`, `random`, `try_start`, `begin`, `find_spot`,
  `spot_try`, `spot_check`, `spawn_horde`, `spawn_member`, `equip`, `give_weapon`, `announce`,
  `lure_tick`, `member_tick`, `maybe_despawn`, `despawn`, and test helpers `start`, `status`, `clear`
- `data/modpack/functions/noise/` (7 functions): `tick` (gunfire detection), `gunshot`, `emit_gun`,
  `new_gun_sense`, `init_gun`, `lure`, `init_lure`
- `data/modpack/predicates/horde/night_or_thunder.json`, `in_structure.json` (67 surface structures:
  villages, outposts, temples, When Dungeons Arise, elytra_dungeons barrow/spire/rift gate)
- `data/elytra_hordes/tags/entity_types/`: `horde_types`, `hostiles`, `gun_bullets` (tacz:bullet,
  optional), `za_senses` (zombieawareness:scent, optional); `tags/blocks/`: `horde_ground`, `horde_air`
- `data/minecraft/tags/functions/load.json` and `tick.json` (merge with elytra_dungeons' tags)
- Scoreboards `mh_cfg mh_const mh_tmp mh_timer mh_cd mh_lure mh_age mh_gun`; entity tags
  `modpack_horde` (horde zombies), `mh_spawn` (world spawn anchor marker), `mh_sense` (pack senses).
  No `ed_` names, no `modpack_boss`/`ed_boss`, no team.

Behaviour: per player in the overworld (survival/adventure, at night or in thunder, at or below Y 150,
not gliding), one 15 % roll per 60 s of eligible time; 15 min cooldown shared within 100 blocks; 8-12
zombies (+1 per extra player within 64, max 16) 40-70 blocks away on natural ground, not in water,
structures, within 100 blocks of world spawn or 96 of a boss arena/rift gate; biome mix (husks in
desert/badlands, some drowned at rivers/beaches/swamps); 2 with iron gear, 20 % of the rest with a
weapon; quiet groan + actionbar "You hear groaning in the distance"; a Zombie Awareness sound sense
at the player every 10 s for 90 s draws the horde in; leftovers removed after 180 s without target and
no player within 64. Gunfire: a new `tacz:bullet` within 8 blocks of a player puts a strength-40
Zombie Awareness sound sense (~26 blocks) at the shooter, max one per second per player.

Validator note: `zombieawareness:scent` and `tacz:bullet` are registered in mod code without lang keys,
so `gamedata.py` does not list them and `packcheck.py` would reject them. The pack therefore uses entity
tags with `"required": false` and summons the sense as a passenger with a single-quoted id, which
packcheck does not inspect. **Added** `questtools/hordecheck.py` to cover that gap: it checks both IDs
in the jars' class files, the scent NBT keys, every `mh_cfg`/`mh_const` value read is set, and every
`mh_*` objective is created (tested with 3 planted errors, all caught). It is not wired into
`validate.py`; teaching `gamedata.py` about code-registered entities would let the pack use plain IDs.

Checks: TOML (tomllib) and pack JSON parse; `validate.py` exit 0 (3 Paxi packs, 0 errors/warnings);
`hordecheck.py` exit 0; `check-mods.ps1` clean. In game: `/reload`, then look for
"Failed to load function modpack:" in `logs/latest.log`.

#### Horde checks in the pre-launch validator (main session, 2026-10-09)
- `questtools/validate.py` now runs `questtools/hordecheck.py` whenever the `elytra_hordes` pack exists and turns its
  errors into launch-blocking errors. hordecheck verifies the code-registered entities `zombieawareness:scent` and
  `tacz:bullet` in the jar classes and checks that every setting used is set and every `mh_*` objective is created.
  Tested by renaming one setting: the launch was blocked, with both functions that use it named.

#### Horde "only 1 zombie" fix (main session, 2026-10-09)
Reported: every horde spawned exactly one zombie.
Cause (my mistake): when testing the horde check I restored `elytra_hordes/.../horde/settings.mcfunction` with
Windows PowerShell `Set-Content -Encoding utf8`, which adds a UTF-8 BOM. Minecraft then failed to load the settings
function (`latest.log`: "Failed to load function modpack:horde/settings ... line 1 ... position 0"), so every
`mh_cfg` setting was unset and the horde size came out as 0 (the spawn loop always makes at least one).
- Removed the BOM; all 24 setting values unchanged.
- `questtools/packcheck.py`: a .mcfunction that starts with a BOM is now a launch-blocking error (tested).
  JSON files with a BOM were already rejected as invalid JSON.
#### Storm Spire rarer (main session, 2026-10-09)
Reported: 3 sky dungeons within 800 blocks.
- `worldgen/structure_set/storm_spire.json`: spacing 28 -> 72 chunks, separation 10 -> 28 (one attempt per
  1,152 x 1,152 blocks, at least 448 blocks apart; about 6x fewer). Only chunks generated from now on are affected.
  Previous pack in `backup/2026-10-09_015653_elytra_dungeons`.
#### Rift Gates rarer (main session, 2026-10-09)
Reported: rift gates as common as the spires were.
- `worldgen/structure_set/rift_gate.json`: spacing 26 -> 64 chunks, separation 10 -> 24 (one attempt per
  1,024 x 1,024 blocks, at least 384 blocks apart; land biomes only). Only chunks generated from now on are affected.

### Phase 4: Boss Dungeons quest chapter (2026-10-09)
- **added** `minecraft/config/ftbquests/quests/chapters/boss_dungeons.snbt` (generated; group Quests, order 6), defined in `questtools/questgen.py`:
  - Ash to Ash: find `elytra_dungeons:ashen_barrow` + advancement `bosses/ashen_warlord` -> SCAR-L + 120 5.56x45
  - Eye of the Storm: find `elytra_dungeons:storm_spire` + `bosses/tempest_herald` -> M107 + 30 .50 BMG
  - Into the Hollow: find `elytra_dungeons:rift_gate` + `bosses/hollow_magus` -> FN Evolys + 96 .308
  No firework rewards. Quests are independent (linear progression would block out-of-order kills).
- **changed** `questtools/gamedata.py`: also indexes Paxi datapacks, so the validator knows the pack's structures, advancements and dimensions.

## Horde leaders (main session, 2026-10-09)
Backup before changes: `backup/leaders-2026-10-09_092505/` (all Paxi datapacks, quest chapters, questgen.py).
- **added** `questtools/leadergen.py`: all numbers in its CONFIG block; writes the leader files into the
  `elytra_hordes` pack (backs up its own files on every run).
- **added** to `config/paxi/datapacks/elytra_hordes/` (75 files): `data/modpack/functions/leader/` (load, loop,
  tick, selection, 6 summon/setup, type AI, Spucker spit, Schreier scream, Kriecher light/grab, Platzer blast,
  death detection via link markers, horde break, despawn, clear, status, force/<type>, here/<type>),
  `loot_tables/leaders/<type>.json`, `advancements/leaders/` (root, kill_any, kill_<type> x6, kriecher_grab),
  `predicates/leader/` (suppressed, lit), `README_leaders.md`
- **changed** in `elytra_hordes`: `data/minecraft/tags/functions/load.json` (+ modpack:leader/load), `tick.json`
  (+ modpack:leader/tick), `horde/spawn_horde.mcfunction` (+ `function modpack:leader/spawn` after the members),
  `horde/clear.mcfunction` (+ `function modpack:leader/clear`)
- **added** chapter `horde_leaders.snbt` (group Quests, **order_index 7**; 8 quests) via `questtools/questgen.py`
- Leaders are tagged `modpack_horde_leader`, `leader_<type>`, `modpack_boss` (NOT `modpack_horde`) and sit on
  teams `ld_<type>` with hidden nametags (glow colour + Neat skips them).
#### Leader fixes and skins (main session, 2026-10-09)
Reported: `here/<type>` spawned leaders 2 blocks underground (they suffocated); custom skins wanted.
- `here/<type>`: the spot is 6 blocks ahead at your feet level (look direction up/down ignored), then steps up
  (max 24) to the first spot with 3 free blocks. New functions `leader/here_find/<type>`.
- **added** `minecraft/mods/entity_texture_features-7.2.4-1.20.1-forge.jar` (Modrinth, SHA-1
  1ee3606828a796d1fdcd90c85c4fb12fc1a36fc4, no dependencies; 7.2.5 skipped as only 5 days old). Client-side: it picks
  textures by a mob's custom name, so only leaders change.
- **added** `minecraft/config/paxi/resourcepacks/elytra_leaders_rp/` (19 files, generated by `leadergen.py`):
  `assets/minecraft/optifine/random/entity/{zombie,zombie_villager}/*.properties` match the leader names, plus the
  recoloured variant textures and `_e` emissive eye textures (eyes glow in the type's colour). Palettes are in
  `PALETTE` in `leadergen.py`.
#### Kriecher visibility (main session, 2026-10-09)
Reported: the Kriecher vanished right after spawning. It turned fully invisible in the dark (by design, too strong). Now: in the dark only the glow and aura are removed (dark skin, squat shape), in light it glows aqua. `leadergen.py` ai/kriecher + kriecher_lit.

#### Kriecher visibility reverted (main session, 2026-10-09)
At the user's request the previous change was undone: the Kriecher is again invisible in the dark (light < 8) and glows in light.

## Portable pre-launch check (2026-10-13)
Reported: on another PC the instance would not start ("Pre-Launch command ... The process failed to start"), because
the pre-launch command pointed at this PC's Python path.
- **added** `questtools/prelaunch.cmd`: runs validate.py via the `py` launcher if Python 3.11+ is installed, otherwise skips
  the check (exit 0). Tested both ways.
- **changed** `instance.cfg`: `PreLaunchCommand=cmd /c $INST_DIR\questtools\prelaunch.cmd` (old value backed up in `backup/`).

## Silent Zombie Awareness resource pack (2026-10-13)
- **added** `minecraft/resourcepacks/Silent Zombie Awareness/`: replaces the sound events `zombieawareness:alert`, `target` and `investigate` with empty sound lists, so they play nothing. Optional: switch it on or off under Options -> Resource Packs.
- Fix (2026-10-13): Prism's instance.cfg is Qt INI, where backslash is an escape character, so `\q`/`\p` were swallowed. The line is now `PreLaunchCommand=cmd /c $INST_DIR\\questtools\\prelaunch.cmd` (escaped backslashes).

## Story rebuilt: "Zwischen den Zeiten" (2026-10-13)
- Chapter `story_ashen_skyways` (file name and ID kept): all 13 old story quests and their lore-book rewards removed (the old book texts are still in `BOOKS` in `questgen.py` for reuse); title is now "Zwischen den Zeiten". The chapter sets `hide_quest_until_deps_complete: true`, so each quest stays invisible until its predecessor is done.
- Quest 1 "Eisern aber weich": advancement `minecraft:story/smelt_iron`, reward `aether:golden_oak_sapling`, German description.
- **added** `questtools/questadd.py` + `questadd.cmd`: interactive quest maker (checks IDs, inserts into questgen.py, regenerates and validates, restores questgen.py automatically on failure).

## Story quest 3 "Schwerter und Kugeln" + Kackhaufen (2026-10-13)
- **added** Paxi datapack `config/paxi/datapacks/elytra_extras/`: recipe `elytra_extras:kackhaufen` (stone sword next to a 9mm round, matched with Forge `partial_nbt` on `AmmoId`) -> a placeable player head "Kackhaufen" (texture "Poop with Flies" from minecraft-heads.com, served by textures.minecraft.net); hidden advancement `elytra_extras:kackhaufen` (`recipe_crafted`). `head_nbt.txt` holds the head NBT for the recipe and the quest icon.
- Quest "Schwerter und Kugeln" in "Zwischen den Zeiten": needs both earlier quests, task = that advancement, no reward, subtitle shows the teaser, description only after completion (`hide_text_until_complete`).

## NPC "Der Bote" (2026-10-13)
- **added** `questtools/messengergen.py` -> `elytra_extras` functions `messenger/*` (+ load/tick tags): a wandering trader on a black horse (NoAI, invulnerable, no despawn), greeting in chat, trades, after a trade asks "Ist das alles was euer Herz begehrt?" with clickable [Ja]/[Nein] (`/trigger mes_answer`); Ja = gallops away and vanishes in smoke, Nein = stays. Trades are placeholders (see CONFIG).
- `questlib.py`: new `command(...)` reward (FTB command reward, default `auto: invisible`, `elevate_perms`). Quest "Schwerter und Kugeln" uses it to summon Der Bote; nothing is shown in its reward list.
- Quest "Kupferpfeil": reward changed from an M9A4 to 1x 9mm round (2026-10-13).
- Der Bote (2026-10-14): the "Triggered [mes_answer]" chat line is hidden. While a question is open the gamerule `sendCommandFeedback` is off (the previous value is remembered); it is restored once nobody has an open question, or after 60 s. New functions `messenger/feedback_off` and `feedback_on`.

## Der Bote: new script and chat look (2026-10-14)
- `messengergen.py` rewritten: greeting -> after 2 s "Ihr seid nicht von hier?" [JA]/[NEIN]. NEIN = 1 heart magic damage, red eyes, warning + question with only [JA]. JA = eyes normal, trades unlock (locked until then: offers kept in storage `elytra_extras:messenger`). After each trade: "Ist das alles…" as before. Lines use a blank line, bold "✦ Der Bote ✦ »", italic text, a trader sound, and big [ JA ] / [ NEIN ] buttons. Trigger values 11/12 (question 1), 21 (question 2), 1/2 (after a trade).
- **added** `config/paxi/resourcepacks/elytra_extras_rp/`: ETF variant `wandering_trader2.png` (+ `_e` emissive) with red eyes, chosen by `name.1=regex:Der Bote.+`. While angry his name gets an invisible no-break space, which switches the texture.
- Der Bote (2026-10-14): after JA he now answers (`after_yes`: "Gut. Dann zeigt mir, was ihr begehrt.") and shows an action-bar hint (`trade_hint`). After every answer the trigger stays enabled and feedback stays hidden for 10 s, so extra clicks no longer show "You cannot trigger this objective yet".

## Der Bote: the deal and the vision (2026-10-14)
- After question 1 (JA): "Alleine schafft ihr es keinen Tag zu überleben. Ich biete euch einen Deal an - arbeitet für mich." [JA]/[NEIN] (trigger 41/42).
  - JA -> deal accepted (placeholder line `after_yes` + trades unlock).
  - NEIN -> infinite blindness, "Lasst mich euch zeigen wo euer Schicksal liegt ohne mich.", 3 s later teleport to the new dimension `elytra_extras:vision` (void with the Hollow's sky, one cracked deepslate tile block at 0 100 0, chunk forceloaded). Blindness cleared, player frozen (movement-speed modifier -100%, jump boost 128, put back on the block every tick), "Seht ihr?" [JA] (31) -> unfreeze, back to the remembered spot (marker + forceload, as for the Rift Gates), facing the Bote, deal accepted.
- **added** `elytra_extras`: `dimension/vision`, `dimension_type/vision`, `worldgen/biome/vision` (written by messengergen.py). A world restart is needed for the new dimension.

## Silence near Der Bote and in custom dimensions (2026-10-14)
- `messenger/tick`: every tick `stopsound ... ambient` for players within 16 blocks of the Bote, in `elytra_extras:vision` and in `elytra_dungeons:the_hollow`. AmbientSounds plays in the ambient category (`useSoundMasterSource: false`) and fades in slowly, so its sounds never become audible there.
- `elytra_extras_rp`: `assets/ambientsounds/basic/dimensions/elytra_silent.json` marks both dimensions as `mute` for AmbientSounds.
- Kackhaufen recipe (2026-10-14): any sword (item tag `#minecraft:swords`: vanilla, Aether incl. lances, Alex's Mobs) + 9mm round; advancement title now "Schwert + 9mm-Patrone".
- Der Bote (2026-10-14): NEIN to question 1 now also gives blindness (lifted when question 2 is answered with JA) and plays one thunder sound (weather category) for that player.
- Silence near Der Bote reworked (2026-10-14): the per-tick `stopsound` let snippets through and is removed. Now the AmbientSounds region `elytra_bote` (resource pack) plays an inaudible sound (`elytra_extras:silence`, vanilla cave1 at volume 0.0001) with `mute: 1`, priority 100, while a wandering trader of team `mes_bote` is within 16 blocks, like the mod's warden region. The Bote joins team `mes_bote`. Custom dimensions stay muted by the `elytra_silent` dimension file.
- Der Bote (2026-10-14): question 1 is now "Ihr seid <player name>, richtig?" (`{player}` in CONFIG `q1`, a `selector: @s` text component sent to each nearby player separately). JA = truth, NEIN = lie (damage, blindness, thunder, red eyes) as before.
- Der Bote (2026-10-14): the warning now ends with "Ich frage euch - Ihr heißt <player name>?" (per-player name, like question 1).

## Der Bote step 4: three wishes and their prices (2026-10-14)
Backup first: backup/bote-wishes-2026-10-14_012031.
- **changed** `questtools/messengergen.py`: CONFIG block "step 4" (all wish texts and numbers); `accept_deal` now asks the
  wish question (stage 5) instead of the placeholder; new `open_shop`; answers 51/52/53 (hook: 54+); functions under
  `messenger/wish/` and new test functions under `messenger/debug/`.
- **added** to `elytra_extras`: `advancements/bote/` (7 impossible-trigger advancements for quests + `kill_villager` /
  `kill_player` with reward function `wish/kill_check`), `predicates/messenger/has_fatigue.json`.
- New scoreboards: mes_wish, mes_price, mes_ptime, mes_pflag, mes_hp, mes_retry, mes_dth (deathCount), mes_bt.
- **changed** `questtools/packcheck.py`: calls to functions in other Paxi datapacks (e.g. `modpack:horde/start`) are valid.- Silence near Der Bote (2026-10-14): the muting sound was a vanilla cave sound at volume 0.0001, which was still audible at intervals. It is now a genuinely silent Ogg Vorbis (`assets/elytra_extras/sounds/silence.ogg`, built by the new `questtools/oggtool.py` from vanilla codec headers + empty frames).
- Der Bote (2026-10-14): after "Ihr werdet von mir hören." he now gallops off and vanishes in smoke after 3 s (`leave_after_farewell_s`) instead of opening his shop. New functions `wish/leave_soon` / `wish/leave_now`. His shop and the trade question remain only for players who meet him after already having chosen a wish.

## Der Zeitbote: atmosphere and control (2026-10-14)
Backup: `backup/bote-atmosphere-2026-10-14_015346/` (datapacks, resourcepacks, messengergen.py).
- `questtools/messengergen.py`: owner model (every Bote belongs to one player: `mes_owner` = `mes_pid`), scene tag `mes_scene`,
  new CONFIG blocks `scene`, `music`, `heartbeat`, `ambient_layer`, `wind`, `vision_slots`; `spawn_ahead` 4 -> 3.
- Scene: invisible seat (armor stand, re-mounted every tick), Resistance V + Fire Resistance + Water Breathing, blind (not in
  the vision); lie damage clears Resistance for that one hit. Ward loops (record category, stops while angry / in the
  vision), quiet random cave + distant bell layer, Bote and horse face the player every tick.
- Failsafes: relog (`mes_leave`), death (`mes_sdth`), Bote missing, max length 600 s (timeout line DRAFT), seats and Botes
  without a scene are removed. New `modpack:bote/force_end` (file `data/modpack/functions/bote/force_end.mcfunction` in elytra_extras).
- Wind: `elytra_extras:wind` (resource pack event pointing at AmbientSounds' `wind/light-wind.ogg`, nothing copied) loops in
  the vision (only sound there) and quietly in the Hollow. Vision biome: mood sound removed (needs a world restart).
- Wishes: prices are chosen as `mes_price 4` and start (`wish/start_price`) only when the scene ends.
- Vision: up to 8 players get separate blocks (x = slot * 1000).
- `questtools/packcheck.py`: also accepts sound events from the Paxi resource packs.
- New test functions `messenger/debug/start|lie|vision|wish|end|force_end|short|state|wind`.
## Rangsystem beim Zeitboten (2026-10-14)
Backup: `backup/ranks-2026-10-14_022512/`.
- New `questtools/rankgen.py` (CONFIG: ranks, thresholds, colours, points, abilities, lines) -> elytra_extras
  `data/modpack/functions/bote/rang/` (49 functions), `advancements/bote/rang/` (root, pakt, siegel_ashen/storm/hollow,
  preis, leader_kill), `predicates/bote/rang/uhr_in_hand`, entity tags `bote/feindlich`, `bote/feindlich_boss`,
  function tag `#modpack:bote/rang_aufstieg` (hook, empty).
- Scoreboards: bote_punkte, bote_rang, bote_ziel, bote_rwait, bote_rkt, bote_rkn, bote_snk, bote_snc, bote_cd6, bote_cd7,
  bote_hp (health), bote_anr. Teams rang_1..rang_7 (prefix = title, friendly fire on). `team remove friends` on load.
- `messengergen.py`: new advancement `elytra_extras:bote/pakt` (granted when the deal is accepted); load/tick tags are
  now merged (both generators add their entries).
- `validate.py`: namespace `modpack` counts as ours (no false "override" warning for our own tags).
- COMMANDS.txt: friends-team note replaced, new section RANGSYSTEM.
## Pfad-Belohnungen Macht / Schutz / Wissen (2026-10-14)
Backup: `backup/pfadbelohnungen-2026-10-14_024711/`.
- New `questtools/pathgen.py` (CONFIG: items, ranks, enchantments, lines) -> elytra_extras `data/modpack/functions/bote/pfad/`
  (112 functions), predicate `bote/pfad/bogen_in_hand`, item modifier `bote/pfad/nbt_zurueck`, function tag
  `#modpack:bote/pfad_handschuh` (required:false), hooks `#modpack:bote/rang_aufstieg` and `#modpack:bote/wunsch_gewaehlt`.
- Loot overrides in elytra_extras `data/aether/loot_tables/chests/dungeon/...` (7 tables, 19 entries removed: all path
  items incl. Phoenix and Valkyrie gloves; obsidian items were in no table). No recipe in any mod makes these items.
- Gloves added at rank 6 (Aether "Require gloves for set abilities" = true in all worlds).
- Phoenix -> Obsidian conversion is reverted (armour slots keep NBT via item modifier; gloves via /curios replace).
- Phoenix Bow: one tagged arrow while held and no other arrow; removed otherwise, killed when dropped.
- Loss: /trigger bote_gabe gives back owed items missing from inventory, armour, ender chest and glove slot (cooldown 1 day).
- messengergen.py: wish/pick calls `#modpack:bote/wunsch_gewaehlt`; add_to_tag() also handles other namespaces.
- rankgen.py: hook tag is merged, no longer overwritten. packcheck.py: function-tag entries with required:false.
## Instance cleanup (2026-10-14)
From now on the notes live in `docs/` (CHANGELOG.md, PROJECT_SUMMARY.md, STATUS.md, COMMANDS.txt, BRIEFING_FOR_CLAUDE_CHAT.md,
devnotes/, cleanup/); older entries above still name the old paths.
- Safety zip `backup/cleanup-2026-10-14_234234.zip`; candidates (old logs/crash reports, configs of removed mods, caches,
  duplicate mod jars in an old backup, TaCZ auto-backup, superseded backups, old generator copies, reports) moved to
  `_to_delete/` with `MANIFEST.json`. Old backups packed into `backup/archive-bis-2026-10-14.zip`.
- `README.md` and `docs/COMMANDS.txt`: paths to docs/ updated. Details and undo: `docs/cleanup/CLEANUP_REPORT.md`.
## Jumpscare mods removed (2026-10-14)
- **moved** minecraft/mods/foxy_jumpscare-0.1-1.20.1.jar, minecraft/mods/witheredfoxy-2.0.0.jar and minecraft/mods/.index/withered-foxy-jumpscare.pw.toml to backup/mods-removed-2026-10-14_234819/ (no other mod depends on them; no config files).

## .packignore (2026-10-14)
- added the line `backup` so Prism exports leave out backup/.

## New instance icon (2026-10-15)
- `PrismLauncher/icons/elysius.png`, instance.cfg `iconKey=elysius`. Icon made by **elisa/sultan**; credited in README.md (Credits), docs/PROJECT_SUMMARY.md and docs/BRIEFING_FOR_CLAUDE_CHAT.md.
