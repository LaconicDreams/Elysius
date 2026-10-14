# Phase 1: worldgen cleanup report (2026-10-08)

Everything below was read from the jars in `minecraft/mods`, the Minecraft 1.20.1 client jar, and `minecraft/config`.
No mod or config file was changed in this phase.

## Folder check (differences from the project summary)
- New in `mods/`: AmbientSounds 6.3.10, CreativeCore 2.12.40 (required by AmbientSounds), AppleSkin 2.5.1.
- Cloth Config is **11.1.136** (the 1.20.1 line), not v10. No installed mod declares a dependency on it.
- No `kubejs/` folder. No global datapack loader. Each world (`Emotional Intelligent`, `first try`, `Kevin`) has an empty `datapacks/` folder.
- Leftovers from removed mods: `config/chunky/`, `config/DistantHorizons.toml`, `config/sophisticatedcore-common.toml`. They are harmless.
- `options.txt`: render distance 16, **simulation distance 8** (the summary recommends 5-6).

## Structures per worldgen mod
"Sets" are structure_set files. Spacing/separation is in chunks; spacing 1 means the set is rolled in every chunk.

| Mod | Structures | Sets | Placement |
|---|---|---|---|
| Vanilla 1.20.1 | 33 | 19 | vanilla |
| When Dungeons Arise 2.1.58 | 39 | 2 | major_structures 60/50 (31 structures), minor_structures 35/25 (6) |
| Repurposed Structures 7.1.25 | 101 | 36 | own `advanced_random_spread`; **mineshafts 1/0 in overworld (9 variants), Nether (3), End, ocean**; outposts 49/24 (10), villages 50/25 (11), pyramids 52/29 (8), witch huts 53/26 (6), ruins 68/30, monuments 91/41 (3), mansions 225/110 (7), plus Nether/End variants. Also **142 placed features**, including 11 biome dungeon variants (badlands, dark_forest, deep, desert, icy, jungle, mushroom, nether, ocean, snow, swamp) and wells. |
| Terralith 2.5.4 | 28 | 7 | 9/6 to 46/18 (underground, rubble, mage towers, rare villages and dungeons) |
| YUNG's Better Dungeons 4.0.4 | 5 | 5 | **small dungeons 10/6**, skeleton 46/23, spider 44/22, zombie 48/24, small Nether 16/10 (off in config) |
| YUNG's Better Mineshafts 4.0.4 | 13 | 1 | 1/0 (replaces vanilla mineshafts) |
| YUNG's Better Strongholds / Fortresses / Desert Temples / Jungle Temples / Ocean Monuments | 1 each | 1 each | replace the vanilla versions |
| The Aether 1.5.2 | 4 | 3 | bronze dungeon 6/5, aerclouds 6/3, silver+gold dungeons 36/24 (Aether only) |

## Where they overlap
| Type | Provided by |
|---|---|
| Mineshafts | YUNG's Better Mineshafts **and** 14 Repurposed Structures mineshafts, both rolled every chunk. This is the biggest duplicated cost. |
| Spawner dungeons | vanilla monster rooms, YUNG's small dungeons (every ~10 chunks), YUNG's skeleton/spider/zombie dungeons, 11 Repurposed Structures dungeon features, Terralith underground dungeon |
| Desert/jungle temples, pyramids | YUNG's (2) and Repurposed Structures pyramids (8 overworld) and temples |
| Ocean monuments | YUNG's and Repurposed Structures (desert, icy, jungle; Nether) |
| Strongholds, fortresses | YUNG's (overworld stronghold, Nether fortress); Repurposed Structures adds Nether/End strongholds and an overworld jungle fortress |
| Villages, outposts, witch huts, igloos, ruins, shipwrecks, mansions | vanilla, Terralith (villages), and Repurposed Structures biome variants of each |
| Big dungeon complexes | When Dungeons Arise only (unique, rare) |

## Proposal (waiting for your OK; nothing is removed yet)

### Option A (recommended): remove Repurposed Structures
- It is the largest generation load: 101 structures, 36 sets and 142 features. Its mineshafts double YUNG's on every chunk, and it overlaps YUNG's in 5 categories plus vanilla in 7.
- **Keep When Dungeons Arise.** Its 39 structures are unique, it spawns rarely (one major structure per ~60x60 chunk region), it is already tiered in the chest loot, and it is the best fit for the boss-dungeon theme.
- **Keep YUNG's Better Dungeons.** It replaces vanilla spawner rooms and is cheap. Once Repurposed Structures is gone, it no longer overlaps anything.
- Effect on existing worlds:
  - Structures that already generated stay as blocks.
  - **Unopened Repurposed Structures chests will be empty**, because their loot tables disappear with the mod.
  - The log will show harmless warnings about unknown structures in old chunks.
- After removal, rerun `py questtools/lootgen.py` so the loot pack drops the Repurposed Structures tables.

### Option B: keep Repurposed Structures, trim it with a datapack
Lithostitched 1.4.11, which is already installed, supports `remove_structure_set_entries` and `remove_features` worldgen modifiers (verified in the jar).
- A datapack could remove the Repurposed Structures mineshafts, dungeon features, pyramids, monuments and temples, and keep its Nether/End content (Nether cities, underground bastions, End structures).
- Downside: datapacks only apply per world (there's no global loader) and only to new chunks. The same applies to the boss dungeons in Phase 2, so see the question below.

### Also proposed
- Optional: remove **Cloth Config**. Nothing depends on it.
- Set simulation distance to 6 (now 8).
- Add **Chunky** for pregeneration (`devnotes/chunky_pregen_commands.md`). It was removed earlier only because it crashed together with Distant Horizons, which is gone now.

## Dependencies and versions (all 48 jars plus 14 bundled)
`check-mods.ps1`: **no missing dependencies, no version mismatches.**
- The Aether 1.5.2 needs Forge 47.1.0+ (you have 47.4.10), Curios 5.3.1+ (5.14.1) and Minecraft 1.20.1. Its libraries are bundled inside it: Cumulus Menus 1.0.1, Nitrogen Internals 1.0.12, MixinExtras, and Curios 5.6.1, which is overridden by your 5.14.1.
- AmbientSounds needs CreativeCore 2.12.36+ (you have 2.12.40).
- Tectonic needs Lithostitched 1.4.11+ (exact match).
- The YUNG's mods need YUNG's API 4.0.1+ (you have 4.0.6).
- Elytra Slot needs Curios 5.2.0+ and Caelus 3.1.0+ (you have 3.2.0).
- FTB Quests and Teams need Architectury 9.1.12+ (you have 9.2.14).
- Alex's Mobs needs Citadel 2.6.0+ (2.6.3). Zombie Awareness needs CoroUtil (1.3.7).
- GeckoLib 4.8.4: no mod declares it as a dependency. Keep it anyway, because Phase 5 custom mobs will use it.
