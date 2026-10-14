# ELYSIUS CODEX – instructions for Claude Code

Generated 2026-10-14 from the Elysius Codex app (first version; the app's Sync tab regenerates a fuller one).

## How to work with this file
- Read it before changing anything. Back up before edits (as you already do); never touch saves, worlds or personal files; ask before deleting.
- Respect the lore and the Lab logic below. If a task conflicts with them, stop and report instead of guessing.
- When you finish work, write `CODEX_UPDATES.json` next to this file (format at the bottom). The user imports it into the app.

## Open work (priority: story first)
- Test in game (all built 2026-10-14, untested): Bote atmosphere, three wishes, ranks, Pfad rewards.
- Verify Aether item IDs and Traveler's Backpack item IDs.
- Quest audit: delete candidates exist (audit/DELETE_CANDIDATES.md); wait for the user's approval.
- Boss: Der Verschlinger (3 phases). Finale "Ein Ende, zwei Entscheidungen" and the Kobold.
- Open design point: does the Kobold also replace the Bote if the player accepted his offer?
- Instance cleanup, horde leaders, Zombie Awareness + roaming hordes (check STATUS.md for what is already done).

## Lore rules (summary)
- Der Bote is a Zeitbote. Player is frozen and immortal while he is present; he always faces the player. Blindness stays on (suspended in the Vision). Quiet "ward" disc plays near him unless he is angry or the player is in his dimension; wind in the Vision and the Hollow.
- Wishes and prices: Macht = kill a player or villager within 3 days. Schutz = mining fatigue for half a day. Wissen = bees chase the player 3 minutes after the encounter.
- Pfad rewards (Aether, unbreakable, uncraftable, unfindable): Macht = Pig Slayer then Obsidian armor, endgame Vampire Blade. Schutz = Hammer of Kingbdogz, Valkyrie armor, endgame Holy Sword. Wissen = Phoenix bow (unlimited arrows), Phoenix armor, endgame Lightning Sword.
- Pacing: small tasks, rewards, bigger tasks (dungeons), then two bosses: Der Verschlinger (frees the world) and the Bote.
- After the finale the Bote is replaced by a Kobold who handles trades and speaks spitefully about the player.
- Focus on story: few side quests and milestones; the big rewards belong to the story.

## Lab logic
```
RULE wahl_macht   WHEN !wunsch_angebot AND chooses(Macht)   THEN set #pfad_macht, emit !preis_macht
RULE wahl_schutz  WHEN !wunsch_angebot AND chooses(Schutz)  THEN set #pfad_schutz
RULE wahl_wissen  WHEN !wunsch_angebot AND chooses(Wissen)  THEN set #pfad_wissen
RULE endgame_loot WHEN #pfad_macht THEN emit !endgame_loot_frei
RULE bote_boss    WHEN !bote_boss_start THEN set #bote_besiegt ELSE set #bote_verschont
RULE kobold       WHEN #bote_besiegt THEN set #kobold_aktiv
```

## Report back: CODEX_UPDATES.json
```json
{
  "tasks_done": ["<task id or exact title>"],
  "tasks_add": [{"title": "", "area": "Story|Bote|Dungeons|Quests|Tech|Polish", "body": ""}],
  "changelog": [{"title": "", "version": "", "kind": "add|change|fix|remove", "text": ""}],
  "findings": [{"title": "", "severity": "high|medium|low", "detail": ""}],
  "ideas": [{"title": "", "area": "Story", "body": ""}]
}
```
