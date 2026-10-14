# Aufräum-Bericht (Phase 2)

Ausgeführt am 2026-10-14 um 23:42, freigegeben: alle S-, W- und U-Punkte, Backup-Archiv, Ordnung in docs/. Endgültig gelöscht wurde **nichts**.

## Was passiert ist

1. **Sicherung:** `backup/cleanup-2026-10-14_234234.zip`. Sie enthält alle verschobenen Dateien und wurde geprüft: lesbar, gleiche Dateianzahl, gleiche Bytes.
2. **Verschoben nach `_to_delete/`** (mit Originalstruktur): 115 Pfade (S1–S7, W1–W8, U1–U2 aus `CLEANUP_PLAN.md`).
3. **Backup-Archiv:** `backup/archive-bis-2026-10-14.zip` (1.7 MB) enthält den Altbestand von 9 Sicherungen (neueste Stände der Reihen + Einzelsicherungen). Geprüft, Originale nach `_to_delete/backup/`.
4. **Ordnung:** `CHANGELOG.md`, `PROJECT_SUMMARY.md`, `BRIEFING_FOR_CLAUDE_CHAT.md`, `COMMANDS.txt`, `STATUS.md`, `devnotes/` und `cleanup/` liegen jetzt in `docs/`. Pfadangaben in `README.md` und `docs/COMMANDS.txt` angepasst; die Aufräum-Skripte finden die Instanz jetzt selbst. `questtools/` und `audit/` bleiben (Pre-Launch-Befehl, Audit-Pfade).
5. **Nicht angefasst:** Datapacks (nicht zusammengelegt), Mods, Configs außer S3/S4, Welten, Screenshots, Prism-Dateien, `.packignore`.

## Platz

| | Größe | Dateien |
|---|---|---|
| vorher (Plan) | 2.39 GB | 13664 |
| jetzt ohne `_to_delete/` und ohne Sicherungs-Zip | **2.03 GB** | **8079** |
| `_to_delete/` (wartet auf deine Bestätigung) | 371.6 MB | 5593 |
| Sicherungs-Zip | 343.4 MB | 1 |
| jetzt insgesamt auf der Platte | 2.73 GB | 13673 |

Nach dem endgültigen Löschen von `_to_delete/` und der Sicherung werden **365.8 MB** frei (bis dahin belegt die Sicherung den Platz doppelt).

## Prüfungen danach

- `questtools/validate.py`: 26 Kapitel, 299 Quests, alle SNBT gültig, IDs eindeutig, alle JSON/mcfunction-Prüfungen ohne Fehler (0 Fehler, 0 Warnungen).
- Kein Verweis in `questtools/`, `audit/`, `minecraft/config/` (inkl. aller Datapacks), `instance.cfg`, `README.md`, `.packignore` zeigt auf eine verschobene Datei. Der Gamedata-Cache und `questtools/backups/` werden von den Werkzeugen selbst neu angelegt.
- Alte Pfade nur noch in historischen CHANGELOG-Einträgen (Absicht: das ist Geschichte).

## Rückgängig machen

- **Alles:** jeden Eintrag aus `_to_delete/MANIFEST.json` zurückschieben (`to` -> `from`), dann `docs/`-Dateien an die alten Orte, und die zwei Pfadzeilen in `README.md` zurück. Oder einfach `backup/cleanup-2026-10-14_234234.zip` im Instanzordner entpacken (alle Pfade im Zip sind relativ zum Instanzordner).
- **Einzelne Datei:** aus `_to_delete/<alter Pfad>` an `<alter Pfad>` zurücklegen.
- **Archiv:** `backup/archive-bis-2026-10-14.zip` in `backup/` entpacken.

## Was noch fehlt

- Dein Testlauf (Welt laden, Quest-Buch, Bote-Szene, Horde). Danach sage ich `_to_delete/` und ggf. das Sicherungs-Zip endgültig weg.
- Offen: `.packignore` um `backup/` erweitern (ein Prism-Export nimmt `backup/` sonst mit).

## Alle Verschiebungen

### Lösch-Kandidaten S/W/U (nach _to_delete/) (115)

- `minecraft/logs/2026-09-30-1.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-1.log.gz`
- `minecraft/logs/2026-09-30-10.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-10.log.gz`
- `minecraft/logs/2026-09-30-2.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-2.log.gz`
- `minecraft/logs/2026-09-30-3.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-3.log.gz`
- `minecraft/logs/2026-09-30-4.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-4.log.gz`
- `minecraft/logs/2026-09-30-5.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-5.log.gz`
- `minecraft/logs/2026-09-30-6.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-6.log.gz`
- `minecraft/logs/2026-09-30-7.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-7.log.gz`
- `minecraft/logs/2026-09-30-8.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-8.log.gz`
- `minecraft/logs/2026-09-30-9.log.gz` -> `_to_delete/minecraft/logs/2026-09-30-9.log.gz`
- `minecraft/logs/2026-10-01-1.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-1.log.gz`
- `minecraft/logs/2026-10-01-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-2.log.gz`
- `minecraft/logs/2026-10-01-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-3.log.gz`
- `minecraft/logs/2026-10-01-4.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-4.log.gz`
- `minecraft/logs/2026-10-01-5.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-5.log.gz`
- `minecraft/logs/2026-10-01-6.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-6.log.gz`
- `minecraft/logs/2026-10-01-7.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-7.log.gz`
- `minecraft/logs/2026-10-01-8.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-8.log.gz`
- `minecraft/logs/2026-10-01-9.log.gz` -> `_to_delete/minecraft/logs/2026-10-01-9.log.gz`
- `minecraft/logs/2026-10-02-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-02-2.log.gz`
- `minecraft/logs/2026-10-05-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-05-2.log.gz`
- `minecraft/logs/2026-10-06-1.log.gz` -> `_to_delete/minecraft/logs/2026-10-06-1.log.gz`
- `minecraft/logs/2026-10-06-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-06-2.log.gz`
- `minecraft/logs/2026-10-06-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-06-3.log.gz`
- `minecraft/logs/2026-10-07-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-07-2.log.gz`
- `minecraft/logs/2026-10-08-1.log.gz` -> `_to_delete/minecraft/logs/2026-10-08-1.log.gz`
- `minecraft/logs/2026-10-08-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-08-2.log.gz`
- `minecraft/logs/2026-10-08-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-08-3.log.gz`
- `minecraft/logs/2026-10-08-4.log.gz` -> `_to_delete/minecraft/logs/2026-10-08-4.log.gz`
- `minecraft/logs/2026-10-09-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-09-2.log.gz`
- `minecraft/logs/2026-10-09-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-09-3.log.gz`
- `minecraft/logs/2026-10-09-4.log.gz` -> `_to_delete/minecraft/logs/2026-10-09-4.log.gz`
- `minecraft/logs/2026-10-09-5.log.gz` -> `_to_delete/minecraft/logs/2026-10-09-5.log.gz`
- `minecraft/logs/2026-10-09-6.log.gz` -> `_to_delete/minecraft/logs/2026-10-09-6.log.gz`
- `minecraft/logs/2026-10-10-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-10-2.log.gz`
- `minecraft/logs/2026-10-13-1.log.gz` -> `_to_delete/minecraft/logs/2026-10-13-1.log.gz`
- `minecraft/logs/2026-10-13-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-13-2.log.gz`
- `minecraft/logs/2026-10-13-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-13-3.log.gz`
- `minecraft/logs/2026-10-13-4.log.gz` -> `_to_delete/minecraft/logs/2026-10-13-4.log.gz`
- `minecraft/logs/2026-10-14-2.log.gz` -> `_to_delete/minecraft/logs/2026-10-14-2.log.gz`
- `minecraft/logs/2026-10-14-3.log.gz` -> `_to_delete/minecraft/logs/2026-10-14-3.log.gz`
- `minecraft/logs/2026-10-14-4.log.gz` -> `_to_delete/minecraft/logs/2026-10-14-4.log.gz`
- `minecraft/logs/2026-10-14-5.log.gz` -> `_to_delete/minecraft/logs/2026-10-14-5.log.gz`
- `minecraft/logs/2026-10-14-6.log.gz` -> `_to_delete/minecraft/logs/2026-10-14-6.log.gz`
- `minecraft/logs/debug-2.log.gz` -> `_to_delete/minecraft/logs/debug-2.log.gz`
- `minecraft/logs/debug-3.log.gz` -> `_to_delete/minecraft/logs/debug-3.log.gz`
- `minecraft/logs/debug-4.log.gz` -> `_to_delete/minecraft/logs/debug-4.log.gz`
- `minecraft/logs/debug-5.log.gz` -> `_to_delete/minecraft/logs/debug-5.log.gz`
- `minecraft/crash-reports/crash-2026-09-30_20.13.50-fml.txt` -> `_to_delete/minecraft/crash-reports/crash-2026-09-30_20.13.50-fml.txt`
- `minecraft/crash-reports/crash-2026-09-30_20.17.13-server.txt` -> `_to_delete/minecraft/crash-reports/crash-2026-09-30_20.17.13-server.txt`
- `minecraft/config/DistantHorizons.toml` -> `_to_delete/minecraft/config/DistantHorizons.toml`
- `minecraft/config/sophisticatedcore-common.toml` -> `_to_delete/minecraft/config/sophisticatedcore-common.toml`
- `questtools/__pycache__` -> `_to_delete/questtools/__pycache__`
- `minecraft/modernfix/structureCacheV1` -> `_to_delete/minecraft/modernfix/structureCacheV1`
- `minecraft/essential/cosmetic-cache` -> `_to_delete/minecraft/essential/cosmetic-cache`
- `backup/2026-10-09_010902_jade_neat/mods/aether-1.20.1-1.5.2-neoforge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/aether-1.20.1-1.5.2-neoforge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/alexsmobs-1.22.9.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/alexsmobs-1.22.9.jar`
- `backup/2026-10-09_010902_jade_neat/mods/AmbientSounds_FORGE_v6.3.10_mc1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/AmbientSounds_FORGE_v6.3.10_mc1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/appleskin-forge-mc1.20.1-2.5.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/appleskin-forge-mc1.20.1-2.5.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/architectury-9.2.14-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/architectury-9.2.14-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/caelus-forge-3.2.0+1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/caelus-forge-3.2.0+1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/Chunky-1.3.146.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/Chunky-1.3.146.jar`
- `backup/2026-10-09_010902_jade_neat/mods/citadel-2.6.3-1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/citadel-2.6.3-1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/coroutil-forge-1.20.1-1.3.7.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/coroutil-forge-1.20.1-1.3.7.jar`
- `backup/2026-10-09_010902_jade_neat/mods/CreativeCore_FORGE_v2.12.40_mc1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/CreativeCore_FORGE_v2.12.40_mc1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/curios-forge-5.14.1+1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/curios-forge-5.14.1+1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/DungeonsArise-1.20.x-2.1.58-release.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/DungeonsArise-1.20.x-2.1.58-release.jar`
- `backup/2026-10-09_010902_jade_neat/mods/elytraslot-forge-6.4.4+1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/elytraslot-forge-6.4.4+1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/embeddium-0.3.31+mc1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/embeddium-0.3.31+mc1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/Essential_1-5-0-1_forge_1-20-1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/Essential_1-5-0-1_forge_1-20-1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/ExplorersCompass-1.20.1-1.4.0-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/ExplorersCompass-1.20.1-1.4.0-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/ferritecore-6.0.1-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/ferritecore-6.0.1-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/foxy_jumpscare-0.1-1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/foxy_jumpscare-0.1-1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/ftb-library-forge-2001.2.13.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/ftb-library-forge-2001.2.13.jar`
- `backup/2026-10-09_010902_jade_neat/mods/ftb-quests-forge-2001.4.22.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/ftb-quests-forge-2001.4.22.jar`
- `backup/2026-10-09_010902_jade_neat/mods/ftb-teams-forge-2001.3.2.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/ftb-teams-forge-2001.3.2.jar`
- `backup/2026-10-09_010902_jade_neat/mods/geckolib-forge-1.20.1-4.8.4.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/geckolib-forge-1.20.1-4.8.4.jar`
- `backup/2026-10-09_010902_jade_neat/mods/jei-1.20.1-forge-15.62.0.219.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/jei-1.20.1-forge-15.62.0.219.jar`
- `backup/2026-10-09_010902_jade_neat/mods/lithostitched-forge-1.20.1-1.4.11.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/lithostitched-forge-1.20.1-1.4.11.jar`
- `backup/2026-10-09_010902_jade_neat/mods/mezz_config-1.20.1-forge-0.6.8.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/mezz_config-1.20.1-forge-0.6.8.jar`
- `backup/2026-10-09_010902_jade_neat/mods/modernfix-forge-5.27.85+mc1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/modernfix-forge-5.27.85+mc1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/NaturesCompass-1.20.1-1.12.0-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/NaturesCompass-1.20.1-1.12.0-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/nyfsspiders-Forge-1.20.1-3.0.2.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/nyfsspiders-Forge-1.20.1-3.0.2.jar`
- `backup/2026-10-09_010902_jade_neat/mods/Paxi-1.20-Forge-4.0.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/Paxi-1.20-Forge-4.0.jar`
- `backup/2026-10-09_010902_jade_neat/mods/Pehkui-3.8.2+1.20.1-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/Pehkui-3.8.2+1.20.1-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/repurposed_structures-7.1.25+1.20.1-forge.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/repurposed_structures-7.1.25+1.20.1-forge.jar`
- `backup/2026-10-09_010902_jade_neat/mods/sodiumdynamiclights-forge-1.0.10-1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/sodiumdynamiclights-forge-1.0.10-1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/sodiumoptionsapi-forge-1.0.10-1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/sodiumoptionsapi-forge-1.0.10-1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/tacz-1.20.1-1.1.8-hotfix2.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/tacz-1.20.1-1.1.8-hotfix2.jar`
- `backup/2026-10-09_010902_jade_neat/mods/tectonic-3.0.17-forge-1.20.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/tectonic-3.0.17-forge-1.20.1.jar`
- `backup/2026-10-09_010902_jade_neat/mods/Terralith_1.20.x_v2.5.4.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/Terralith_1.20.x_v2.5.4.jar`
- `backup/2026-10-09_010902_jade_neat/mods/travelersbackpack-forge-1.20.1-9.1.57.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/travelersbackpack-forge-1.20.1-9.1.57.jar`
- `backup/2026-10-09_010902_jade_neat/mods/veinminer-1.1.0.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/veinminer-1.1.0.jar`
- `backup/2026-10-09_010902_jade_neat/mods/witheredfoxy-2.0.0.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/witheredfoxy-2.0.0.jar`
- `backup/2026-10-09_010902_jade_neat/mods/xaerominimap-forge-1.20.1-26.6.0.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/xaerominimap-forge-1.20.1-26.6.0.jar`
- `backup/2026-10-09_010902_jade_neat/mods/xaeroworldmap-forge-1.20.1-1.47.0.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/xaeroworldmap-forge-1.20.1-1.47.0.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsApi-1.20-Forge-4.0.6.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsApi-1.20-Forge-4.0.6.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterDesertTemples-1.20-Forge-3.0.3.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterDesertTemples-1.20-Forge-3.0.3.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterDungeons-1.20-Forge-4.0.4.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterDungeons-1.20-Forge-4.0.4.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterJungleTemples-1.20-Forge-2.0.5.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterJungleTemples-1.20-Forge-2.0.5.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterMineshafts-1.20-Forge-4.0.4.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterMineshafts-1.20-Forge-4.0.4.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterNetherFortresses-1.20-Forge-2.0.6.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterNetherFortresses-1.20-Forge-2.0.6.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterOceanMonuments-1.20-Forge-3.0.4.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterOceanMonuments-1.20-Forge-3.0.4.jar`
- `backup/2026-10-09_010902_jade_neat/mods/YungsBetterStrongholds-1.20-Forge-4.0.3.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/YungsBetterStrongholds-1.20-Forge-4.0.3.jar`
- `backup/2026-10-09_010902_jade_neat/mods/zombieawareness-1.20.1-1.13.1.jar` -> `_to_delete/backup/2026-10-09_010902_jade_neat/mods/zombieawareness-1.20.1-1.13.1.jar`
- `minecraft/tacz_backup` -> `_to_delete/minecraft/tacz_backup`
- `questtools/backups` -> `_to_delete/questtools/backups`
- `questtools/.gamedata_cache.json` -> `_to_delete/questtools/.gamedata_cache.json`
- `questtools/validate_report.txt` -> `_to_delete/questtools/validate_report.txt`
- `questtools/balance_report.txt` -> `_to_delete/questtools/balance_report.txt`
- `questtools/loot_report.txt` -> `_to_delete/questtools/loot_report.txt`
- `mod-check-report.txt` -> `_to_delete/mod-check-report.txt`
- `minecraft/XaeroWaypoints_BACKUP240807` -> `_to_delete/minecraft/XaeroWaypoints_BACKUP240807`
- `minecraft/local/ftbquests/saved` -> `_to_delete/minecraft/local/ftbquests/saved`
- `exports` -> `_to_delete/exports`

### alte Backups (nach _to_delete/, Inhalt im Archiv oder W3/W4) (33)

- `backup/2026-10-09_001517_elytra_dungeons` -> `_to_delete/backup/2026-10-09_001517_elytra_dungeons`
- `backup/2026-10-09_002149_elytra_dungeons` -> `_to_delete/backup/2026-10-09_002149_elytra_dungeons`
- `backup/2026-10-09_003859_elytra_dungeons` -> `_to_delete/backup/2026-10-09_003859_elytra_dungeons`
- `backup/2026-10-09_005047_elytra_dungeons` -> `_to_delete/backup/2026-10-09_005047_elytra_dungeons`
- `backup/2026-10-09_005832_elytra_dungeons` -> `_to_delete/backup/2026-10-09_005832_elytra_dungeons`
- `backup/2026-10-09_010707_elytra_dungeons` -> `_to_delete/backup/2026-10-09_010707_elytra_dungeons`
- `backup/2026-10-09_011549_elytra_dungeons` -> `_to_delete/backup/2026-10-09_011549_elytra_dungeons`
- `backup/2026-10-09_011737_elytra_dungeons` -> `_to_delete/backup/2026-10-09_011737_elytra_dungeons`
- `backup/2026-10-09_013625_elytra_dungeons` -> `_to_delete/backup/2026-10-09_013625_elytra_dungeons`
- `backup/2026-10-09_015653_elytra_dungeons` -> `_to_delete/backup/2026-10-09_015653_elytra_dungeons`
- `backup/2026-10-09_010708_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_010708_elytra_dungeons_rp`
- `backup/2026-10-09_011550_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_011550_elytra_dungeons_rp`
- `backup/2026-10-09_011737_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_011737_elytra_dungeons_rp`
- `backup/2026-10-09_013626_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_013626_elytra_dungeons_rp`
- `backup/2026-10-09_015653_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_015653_elytra_dungeons_rp`
- `backup/leaders-2026-10-09_092505` -> `_to_delete/backup/leaders-2026-10-09_092505`
- `backup/leaders-2026-10-09_213900` -> `_to_delete/backup/leaders-2026-10-09_213900`
- `backup/leaders-2026-10-09_214620` -> `_to_delete/backup/leaders-2026-10-09_214620`
- `backup/leaders-2026-10-09_214642` -> `_to_delete/backup/leaders-2026-10-09_214642`
- `backup/leaders-2026-10-09_215835` -> `_to_delete/backup/leaders-2026-10-09_215835`
- `backup/leaders-rp-2026-10-09_214642` -> `_to_delete/backup/leaders-rp-2026-10-09_214642`
- `backup/leaders-rp-2026-10-09_215835` -> `_to_delete/backup/leaders-rp-2026-10-09_215835`
- `backup/instance.cfg.2026-10-13_005850.bak` -> `_to_delete/backup/instance.cfg.2026-10-13_005850.bak`
- `backup/instance.cfg.2026-10-13_011616.bak` -> `_to_delete/backup/instance.cfg.2026-10-13_011616.bak`
- `backup/2026-10-08_233121_phase1` -> `_to_delete/backup/2026-10-08_233121_phase1`
- `backup/2026-10-09_010902_jade_neat` -> `_to_delete/backup/2026-10-09_010902_jade_neat`
- `backup/2026-10-09_011607_configure_hud` -> `_to_delete/backup/2026-10-09_011607_configure_hud`
- `backup/2026-10-09_015812_elytra_dungeons` -> `_to_delete/backup/2026-10-09_015812_elytra_dungeons`
- `backup/2026-10-09_015813_elytra_dungeons_rp` -> `_to_delete/backup/2026-10-09_015813_elytra_dungeons_rp`
- `backup/kackhaufen_recipe_20261014_005254.json` -> `_to_delete/backup/kackhaufen_recipe_20261014_005254.json`
- `backup/leaders-2026-10-09_220536` -> `_to_delete/backup/leaders-2026-10-09_220536`
- `backup/leaders-rp-2026-10-09_220536` -> `_to_delete/backup/leaders-rp-2026-10-09_220536`
- `backup/zombie-2026-10-09_012900` -> `_to_delete/backup/zombie-2026-10-09_012900`

### nach docs/ verschoben (6)

- `CHANGELOG.md` -> `docs/CHANGELOG.md`
- `PROJECT_SUMMARY.md` -> `docs/PROJECT_SUMMARY.md`
- `BRIEFING_FOR_CLAUDE_CHAT.md` -> `docs/BRIEFING_FOR_CLAUDE_CHAT.md`
- `COMMANDS.txt` -> `docs/COMMANDS.txt`
- `STATUS.md` -> `docs/STATUS.md`
- `devnotes` -> `docs/devnotes`

