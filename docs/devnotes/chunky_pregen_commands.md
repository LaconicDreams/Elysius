# Chunky pregeneration commands

**Not installed yet.** Get the latest Chunky build for **Forge 1.20.1** from Modrinth or CurseForge (author: pop4959) and put it in `minecraft/mods`.
Your old `config/chunky/config.json` is still there. Change `"continueOnRestart": false` to `true` so a pregen that gets interrupted resumes on the next start.

## Do this last
Structures, including the boss dungeons from Phase 2 and 3, only generate in chunks created **after** their mod or datapack is installed.
Pregenerate only once the mod list and the datapack are final. Pregenerate each world separately.

## Commands (run as an operator, in the world you will play)
Dimension IDs were checked in the jars: `minecraft:overworld`, `minecraft:the_nether`, `minecraft:the_end`, `aether:the_aether`.

```
# Overworld: 5000-block radius around spawn (about 390,000 chunks)
/chunky world minecraft:overworld
/chunky shape square
/chunky spawn
/chunky radius 5000
/chunky start

# Nether: 1500 blocks (1500 Nether blocks = 12,000 overworld blocks of travel)
/chunky world minecraft:the_nether
/chunky center 0 0
/chunky radius 1500
/chunky start

# Aether: 3000 blocks
/chunky world aether:the_aether
/chunky center 0 0
/chunky radius 3000
/chunky start

# Optional, the End (outer islands start ~1000 blocks out; End cities)
/chunky world minecraft:the_end
/chunky center 0 0
/chunky radius 3000
/chunky start
```

Chunky queues one task per dimension. Useful commands while it runs:
```
/chunky progress     show progress and estimated time left
/chunky pause        stop for now (resume with /chunky continue)
/chunky cancel       drop the queued tasks
```

## Expectations
- With Terralith, Tectonic and the structure mods, expect **several hours** for the overworld at radius 5000, and several GB of disk space. Check `/chunky progress` after a few minutes for a real estimate on your PC.
- Let it run with nobody flying around. Lower render distance during the run.
- If you only want to test, a radius of 2000 is about 6x faster.
