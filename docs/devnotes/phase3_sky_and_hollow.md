# Phase 3: Storm Spire, Rift Gates and the Hollow

Built by `questtools/dungeongen.py` + `questtools/dungeons_p3.py` into the same Paxi datapack (`elytra_dungeons`).
**Restart the world after updating** (worldgen and dimensions are only read when a world loads; `/reload` is not enough).
Minecraft may show an "Experimental Settings" warning when loading a world that uses a datapack dimension. That is
normal for datapack dimensions; choose Proceed.

## Storm Spire, v2 "Tempest Crown" (sky arena, elytra only), redesigned 2026-10-09
- Floating island at about **y=225 to 241**: a **39-block-wide** circular arena on top (calcite with a copper ring,
  cyan sigil lines, sea lanterns), a low quartz rim with openings to the north, south, east and west, and 8
  lightning-rod columns at the very edge (out of the line of fire). Roots hang under the island.
- **Landing dock** on the south side with the **rocket resupply barrel**: it refills with 4 stacks (256 rockets) whenever a player
  is within 6 blocks and it has none left (60 s cooldown; anything else stored in it is replaced).
- **Vault** inside the island: trapdoor in the floor just south of the centre, ladder down, loot chest.
- Spawns over oceans, forests, taiga, jungle, savanna, beaches, rivers, plains, meadow, desert, swamp, snowy plains
  and mushroom fields (no mountains). Spacing 72, separation 28 chunks (about one per 1,150 x 1,150 blocks).
- The v1 piece (`storm_spire/spire`) stays in the pack only so spires generated before the redesign still load.

**Boss: Tempest Herald** (400 HP; custom storm-ghast model from the resource pack over an invisible ghast hitbox; scripted movement and attacks)
| Mechanic | Detail |
|---|---|
| Flight | Circles the arena 10 blocks from the centre and 11 blocks up, always facing the nearest player. He never leaves the platform area, so his drops land on it. |
| Attack | An aimed fireball at the nearest player every 3 s (2 s in phase 2). The fireballs don't break blocks. |
| Weak point | The **ruby on his forehead** (red sparkles). Its invisible hitbox sits just in front of his face, which always turns toward you. His body has Resistance IV and takes 20%. Damage on the ruby is dealt to him **x3**, then the ruby heals. If one big hit destroys it, a new one forms. |
| Waves | 3 **Storm Riders** (fire-resistant phantoms) every 30 s; 4 every 25 s in phase 2 |
| Phase 2 (200 HP) | Every 5 s a random player's spot gets **sparks and a light column**; lightning strikes there 1 s later. Move! |
| Reset / victory | Resets when everyone is 64+ blocks away. Victory: reward chest at the centre, boss drops, advancement `elytra_dungeons:bosses/tempest_herald` |

Drops: AI AWP (30 rounds of .338) or MK14 / SCAR-H (48 rounds of .308), 3 ghast tears, 4 phantom membranes.
Reward chest: diamonds, emeralds, ghast tears, 50% netherite scrap, 20% totem, books, high-end scopes, 64 rockets.
## Rift Gates and the Hollow (separate dimension)
- **Rift Gate** (overworld): a ruined crying-obsidian frame with portal particles. Forests, taiga, jungle, savanna,
  badlands, plains, meadow, desert, swamp, snowy plains, dark forest. Spacing 64, separation 24 (about one per 1,024 x 1,024 blocks of land).
- **Step into the frame** and you are taken to `elytra_dungeons:the_hollow`: a void with an End-style sky.
  A return marker is saved 3 blocks in front of the gate you used (its chunk stays loaded while you are away).
- Datapacks cannot add new blocks, so the "portal" is the frame plus a function that teleports anyone standing in it.
  5 s cooldown so you don't bounce straight back.
- **The arena** is placed once, on the first visit, at x -20..20, y 80..90, z -20..20. Its chunks stay
  force-loaded so the fight logic always runs.
  - Fall below y=70 and you are put back at the arrival point with 2 hearts of damage (no void deaths, no lost items).
  - The **return rift** on the south edge sends you back to the gate you came through.
  - Dying in the Hollow clears your return point; you respawn as normal.

**Boss: Hollow Magus** (illusioner with a void-purple skin from the resource pack, **2x size** via Pehkui, 500 HP, Power II bow, blindness and decoys from vanilla illusioner AI, plus scripted **evoker-fang lines** at the nearest player every 4 s)
| Mechanic | Detail |
|---|---|
| Shield | Immune (Resistance V) while any of the **4 end crystals** on the diagonal pillars exists. Shoot all 4 (from range: they explode) and the shield drops for **15 s**: he glows, and an **ammo drop** (5.56, .308, 12 gauge, 9mm) lands on the altar. Then the shield and crystals come back. |
| Waves | 3 vexes every 20 s (+1 in phase 2, +1 in phase 3); they expire after 30 s |
| Phase 2 (330 HP) | Speed, extra vex wave |
| Phase 3 (160 HP) | **Void pulse** every 6 s: everyone within 7 blocks is thrown upward (keep your elytra ready) |
| After a win | Reward chest + drops; he returns once nobody has been in the arena for 10 minutes |

Drops: M249 (60 rounds of 5.56), SPAS-12 or AA-12 (36 rounds of 12 gauge) or Vector 45 (60 rounds of .45 ACP), 4 ender pearls.
Reward chest: diamonds, emeralds, 40% netherite ingot, echo shards, 50% totem, books, top-tier attachments, 3 ammo stacks.
The arena is built from obsidian and crying obsidian so the crystal explosions don't destroy it.

## Test commands
```
/locate structure elytra_dungeons:storm_spire
/place structure elytra_dungeons:storm_spire
/locate structure elytra_dungeons:rift_gate
/place structure elytra_dungeons:rift_gate
/function elytra_dungeons:debug/hollow_enter
/function elytra_dungeons:debug/herald_here
/function elytra_dungeons:debug/rearm
/function elytra_dungeons:debug/hollow_rebuild
```
- `/place structure ...storm_spire` builds the Crown **above you at y=225** (about 245 for the arena floor). Fly up.
  Spires placed before the redesign keep the old small platform; place a new one to test v2.
- `debug/hollow_enter` takes you to the Hollow without a gate; the return rift brings you back to where you ran it.
- `debug/rearm` restarts any boss within 64 blocks (works in the Hollow too).
- `debug/hollow_rebuild` re-places the Hollow arena on the next visit (only needed after I change the arena).

## Not verifiable outside the game (please check)
- **TaCZ bullets hit the Storm Core (now floating above the Herald) and the end crystals.** Both are normal entities, so
  they should. This is the main thing to confirm.
- The scripted fireballs fly toward you and don't break blocks.
- The phantoms survive daylight (fire resistance).
- The Hollow loads as a dimension through Paxi, and the arena is placed on the first visit (a short
  "The rift tears open..." message, then you arrive).
- Balance: core multiplier x3, Resistance IV, 400 / 500 HP, crystal shield 15 s, wave sizes.
