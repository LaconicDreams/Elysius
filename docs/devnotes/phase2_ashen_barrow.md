# Phase 2: Ashen Barrow (first boss dungeon)

Datapack: `minecraft/config/paxi/datapacks/elytra_dungeons`, built by `questtools/dungeongen.py`.
Edit the generator, not the pack; the pack is rebuilt (and the old one backed up) on every run.

## The dungeon
- **Where:** `#minecraft:is_badlands`, `#minecraft:is_savanna`, `minecraft:desert`, plus Terralith ashen_savanna,
  basalt_cliffs, volcanic_crater, volcanic_peaks, bryce_canyon, savanna_badlands, white_mesa, desert_canyon
  (marked optional, so the pack still loads without Terralith).
- **How rare:** structure set random_spread, spacing 24, separation 8 chunks (one attempt per 384x384 blocks; it spawns if the biome at the surface matches).
  Also Terralith arid_highlands, fractured_savanna, savanna_slopes, sandstone_valley, desert_spires, scarlet_mountains, warped_mesa, gravel_desert.
- **Layout** (jigsaw, 4 pieces):
  1. `ruin` (11x9x11, start piece at ground level): a ruined blackstone ring around the shaft opening.
     A vertical jigsaw attaches the shaft below it.
  1b. `shaft` (11x19x11): a spiral stair runs down the walls. A 3x3 water pool at the bottom lets you **jump or glide straight down** without fall damage.
     (`entrance` is the old single-piece version, kept only for barrows generated before 2026-10-09.)
  2. `corridor_a` / `corridor_b` (7x7x15, picked at random): `b` has a loot chest and a skeleton spawner,
     `a` has barred cells.
  3. `arena` (25x14x25): basalt pillars, a throne dais on the north side, and a marker entity in the middle that
     starts the fight.
- Block decay processor: 15-25% of the bricks become cracked variants.

## The fight
| Trigger | What happens |
|---|---|
| A player comes within 10 blocks of the arena centre | **Ashen Warlord** spawns at the throne: wither skeleton, 300 HP, netherite sword (Sharpness III, Fire Aspect), trimmed netherite helmet and chestplate, 85% knockback resistance. Boss bar. Wave 1: 4 skeleton archers in the corners. |
| HP 200 or less (phase 2) | Speed I. Wave 2: 3 wither skeleton guards + **Ash Captain** (80 HP, iron gear). |
| HP 100 or less (phase 3, enraged) | Strength I, burning look, and a fire nova every 4 s: 6 damage to anyone within 4 blocks of him. |
| Boss leaves the arena (18+ blocks from the centre) | He is pulled back to the centre. |
| Every player is 48+ blocks away | The fight resets: boss and adds vanish with no drops, the arena goes back to sleep. |
| Boss dead while players are near | Reward chest appears in the middle of the arena, boss drops land on it, advancement `elytra_dungeons:bosses/ashen_warlord` for everyone within 48 blocks, the remaining adds die. |

**Boss drops** (`loot_tables/boss/ashen_warlord.json`): one of FN FAL, HK G3 (each with 48 rounds of .308) or
M1014 (36 rounds of 12 gauge), plus a wither skeleton skull and bones.
**Reward chest:** 3-6 diamonds, 4-10 emeralds, 6-12 gold, 35% netherite scrap, golden apples, 2 enchanted books,
1-2 attachments, a stack of .308 or 12 gauge.
**Corridor chest:** bones, coal, iron, gold, gunpowder, arrows, soul torches; 50% ammo; 15% a cheap attachment.

## Test commands (operator, cheats on)
```
/reload
/locate structure elytra_dungeons:ashen_barrow
/place structure elytra_dungeons:ashen_barrow
/function elytra_dungeons:debug/warlord_here
/function elytra_dungeons:debug/clear_markers
/place template elytra_dungeons:ashen_barrow/arena ~ ~ ~
```
- `/place structure` builds the whole dungeon at your position (it ignores biomes). Stand on flat ground; the shaft
  goes 20 blocks down.
- `/locate` only finds barrows in chunks that generate from now on, and only in the biomes above.
- `debug/warlord_here` places an arena trigger where you stand, so you can test the fight without the structure:
  walk 15+ blocks away, then come back.
- `debug/clear_markers` stops any fight within 32 blocks and removes the triggers.
- Placing a single `arena` template also places its trigger marker.

## Verified against the jars
Every block state (1,252 known), entity, item, enchantment, effect, particle, sound, trim pattern/material, biome,
biome tag, TaCZ gun/ammo/attachment ID and fire mode used here is checked by `dungeongen.py` and again by
`validate.py` before launch.

## Not verifiable outside the game (please check)
- The arena marker spawns with the structure. Vanilla villages place animals the same way, so it should.
  Check: `/execute if entity @e[type=marker,tag=ed_warlord]` near a fresh barrow.
- Balance: 300 HP against TaCZ guns, the fire nova damage, the wave sizes. Values are at the top of `ab_functions`
  and in `WARLORD_NBT` in `dungeongen.py`.
- Command syntax is checked by the game itself: after `/reload`, any broken line appears in `logs/latest.log`.
