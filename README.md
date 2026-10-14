# Elysius

**An elytra survival modpack for Minecraft 1.20.1 (Forge).** The sun has gone dark. You wake up with a pair of
wings that won't break, a logbook that isn't yours, and a world full of the dead. Fly across a huge reworked
world, hunt bosses in ruins, sky towers and a dimension of their own, and fight roaming zombie hordes with real
guns.

![Minecraft](https://img.shields.io/badge/Minecraft-1.20.1-green) ![Forge](https://img.shields.io/badge/Forge-47.4.10-orange) ![Mods](https://img.shields.io/badge/mods-53-blue)

---

## Features

### Wings first
- Every player starts with an **unbreakable elytra**, a stack of rockets and a Traveler's Backpack.
  Elytra and backpack share the back slot.
- Rockets are traded for gunpowder, bones and rotten flesh, so you never stay grounded.
- Sky structures and a floating boss arena are only reachable by air.

### Guns (TaCZ)
- 53 guns, 24 calibres and 95 attachments, all bought through the quest-book shop with gold, diamonds and
  emeralds.
- Every ammo trade comes as a single buy and a one-click full stack. Handguns and slow-firing guns cost less
  ammo per round.
- Dungeon and structure chests in every dimension contain guns, attachments and ammo, rarer and stronger the
  more dangerous the place.

### Boss dungeons
| Dungeon | Where | Boss | The trick |
|---|---|---|---|
| **Ashen Barrow** | A ruin in badlands, desert and volcanic biomes; a shaft leads down to a throne hall | **Ashen Warlord**: a netherite-clad wither skeleton | Three phases, guard waves, and a fire nova when enraged |
| **Tempest Crown** | A floating island at cloud height, elytra only, with a rocket resupply dock | **Tempest Herald**: a storm ghast | Only the **ruby on its forehead** takes real damage, and lightning hunts you in phase 2 |
| **The Hollow** | A void dimension behind crying-obsidian **Rift Gates** | **Hollow Magus**: a giant void sorcerer | Shoot the four **end crystals** to break his shield, dodge fang lines, and keep your wings ready for the void pulse |

Every boss drops a gun with matching ammo and a reward chest, and has its own quest.

### Zombie hordes
- Hordes of 8–16 zombies roam the overworld at night: husks in deserts, drowned near water, some in armour.
- You hear them groan before you see them. Gunfire draws nearby zombies in.
- Every horde is led by one of six **leaders**, each with its own skin, glow colour, bossbar and weakness:

| Leader | What it does | Counter |
|---|---|---|
| **Läufer** | Sprints at you once it sees you | Shotgun |
| **Brecher** | Armoured tank, barely feels body shots | Armour-piercing guns and ammo, headshots |
| **Spucker** | Throws poison from range | Sniper rifle |
| **Schreier** | Screams to call more zombies | Suppressor, kill it first |
| **Kriecher** | Invisible in the dark, grabs your legs | Light the area up |
| **Platzer** | Explodes when it dies | Keep your distance |

- Kill the leader and the horde scatters.

### Quests (FTB Quests)
26 chapters and over 300 quests, including:
- a story chapter (*The Ashen Skyways*) with written lore books
- flight challenges and bounty hunts in the Overworld, Nether, Aether and End
- good deeds, long-term goals, backpack upgrades
- the gun, ammo and attachment shop
- the Boss Dungeons and Horde Leaders chapters

### A bigger, stranger world
- **Terralith** and **Tectonic** terrain, **The Aether**.
- **YUNG's** reworked structures and **When Dungeons Arise**, plus **Repurposed Structures**, trimmed so it
  doesn't duplicate YUNG's.
- **Alex's Mobs**, smarter zombies (**Zombie Awareness**), climbing spiders, and a few jump scares for the
  unwary.

---

## Installation

1. Install [Prism Launcher](https://prismlauncher.org/).
2. Download the latest release zip from this repository.
3. In Prism, choose **Add Instance → Import** and select the zip.
4. Give the instance **at least 6 GB of RAM** (Edit → Settings → Java). Java 17 is required.
5. Start the game.

**Multiplayer:** everyone needs the same pack. The bundled resource packs and Entity Texture Features provide
the boss and leader skins; without them you still play normally but see vanilla mobs.

**Recommended:** pregenerate your world with Chunky before a long session. Flying into new terrain is fast, and
heavy worldgen can't always keep up. The commands are in `docs/devnotes/chunky_pregen_commands.md`.

---

## Mod list

| Category | Mods |
|---|---|
| Flight and gear | Elytra Slot, Caelus API, Curios API, Traveler's Backpack |
| Guns | Timeless and Classics Guns: Zero (TaCZ) |
| World | Terralith, Tectonic, Lithostitched, The Aether, When Dungeons Arise, Repurposed Structures, YUNG's API + Better Desert Temples, Dungeons, Jungle Temples, Mineshafts, Nether Fortresses, Ocean Monuments, Strongholds |
| Mobs | Alex's Mobs, Citadel, Zombie Awareness, CoroUtil, Nyf's Spiders, GeckoLib |
| Quests | FTB Quests, FTB Teams, FTB Library, Architectury |
| Interface | JEI, Jade, Neat, AppleSkin, Xaero's Minimap, Xaero's World Map, Explorer's Compass, Nature's Compass, Mezz Config |
| Visuals and sound | Entity Texture Features, Pehkui, Sodium Dynamic Lights, Sodium Options API, AmbientSounds, CreativeCore |
| Performance and tools | Embeddium, ModernFix, FerriteCore, Chunky, Paxi, Veinminer, Essential |

All mods belong to their respective authors and are downloaded under their own licenses.

## Credits

- Pack icon: made by **elisa/sultan**.

---

## For pack developers

The custom content is generated by Python 3.12 scripts in `questtools/`. Edit the scripts, not the generated
files.

| Script | What it builds |
|---|---|
| `questgen.py` | All FTB Quests chapters from one data table: stable IDs, escaping, stack splitting |
| `dungeongen.py` | The boss dungeon datapack (structures, worldgen, fight logic, loot) and its resource pack |
| `leadergen.py` | The horde leaders, their loot, advancements and skins. Every number is in one CONFIG block |
| `lootgen.py` | Guns, attachments and ammo in structure chests (TaCZ loot injectors) |
| `balance.py` | Economy audit of shop prices and rewards |
| `validate.py` | Pre-launch check of quests, datapacks, resource packs and loot (runs before every launch) |

- `check-mods.ps1` checks every jar for missing dependencies and version mismatches.
- `docs/COMMANDS.txt` lists every in-game test and admin command.
- `docs/CHANGELOG.md` records every change.
