# Aufräum-Plan (Phase 1: nur Bestandsaufnahme, es wurde NICHTS geändert)

Erzeugt von `cleanup/plan_inventory.py` am 2026-10-14 03:12. Alle Größen sind gemessen.

## 1. Übersicht

Instanz gesamt: **2.39 GB**, 13664 Dateien.

| Instanzordner | Größe | Dateien | Zweck |
|---|---|---|---|
| .packignore | 0.0 KB | 1 |  |
| BRIEFING_FOR_CLAUDE_CHAT.md | 7.3 KB | 1 |  |
| CHANGELOG.md | 39.1 KB | 1 |  |
| COMMANDS.txt | 11.4 KB | 1 |  |
| PROJECT_SUMMARY.md | 7.5 KB | 1 |  |
| README.md | 6.2 KB | 1 |  |
| STATUS.md | 2.5 KB | 1 |  |
| audit/ | 91.8 KB | 5 | Quest-Audit (Bericht + Skripte) |
| backup/ | 290.0 MB | 4348 | unsere Sicherungen (von Hand und von den Generatoren) |
| check-mods.ps1 | 16.3 KB | 1 |  |
| cleanup/ | 20.2 KB | 1 | dieser Plan |
| devnotes/ | 19.1 KB | 4 | Phasen-Notizen der Boss-Dungeons |
| elytra_pack_icon.png | 7.5 KB | 1 |  |
| exports/ | 0.4 KB | 1 | exportierte Ressourcenpaket-Zips |
| instance.cfg | 1.8 KB | 1 |  |
| minecraft/ | 2.11 GB | 9200 | das Spiel (Prism-Ordner .minecraft) |
| mmc-pack.json | 1.0 KB | 1 |  |
| mod-check-report.txt | 0.4 KB | 1 |  |
| questtools/ | 2.0 MB | 93 | Generatoren und Prüfer (Quests, Datapacks, Validator; Pre-Launch-Befehl zeigt hierher) |

| minecraft/… | Größe | Dateien | Zweck |
|---|---|---|---|
| XaeroWaypoints_BACKUP240807/ | 0.6 KB | 2 | Xaero-eigene Sicherung alter Wegpunkte |
| config/ | 1.0 MB | 850 | Mod-Einstellungen, Quests, Paxi-Datapacks |
| coremods/ | 0.0 KB | 0 |  |
| crash-reports/ | 70.3 KB | 3 | Absturzberichte |
| defaultconfigs/ | 0.3 KB | 2 | Standard-Configs für neue Welten |
| essential/ | 74.7 MB | 2281 | Essential-Mod: Loader, Bibliotheken, Caches |
| icon.png | 1.8 KB | 1 |  |
| local/ | 1.6 KB | 4 | lokale FTB-Einstellungen |
| logs/ | 2.3 MB | 52 | Spiel-Logs |
| modernfix/ | 15.7 MB | 503 | ModernFix-Cache (Strukturen) |
| mods/ | 286.6 MB | 103 | Mod-Jars (+ .index von Prism) |
| ops.json | 0.4 KB | 1 |  |
| options.txt | 9.2 KB | 1 |  |
| resourcepacks/ | 0.3 KB | 2 | Ressourcenpakete |
| saves/ | 1.51 GB | 1462 | Welten (Spielstände) |
| screenshots/ | 12.8 MB | 8 | Screenshots des Spielers |
| server-resource-packs/ | 0.0 KB | 0 |  |
| shaderpacks/ | 0.0 KB | 0 |  |
| tacz/ | 77.0 MB | 3331 | TaCZ-Waffenpakete (Standardpaket + elytra_loot) |
| tacz_backup/ | 49.2 MB | 1 | automatische Sicherung des TaCZ-Standardpakets |
| texturepacks/ | 0.0 KB | 0 |  |
| usercache.json | 0.6 KB | 1 |  |
| usernamecache.json | 0.2 KB | 1 |  |
| whitelist.json | 0.3 KB | 1 |  |
| xaero/ | 93.1 MB | 590 | Xaero Minimap/Weltkarte (Kartendaten, Wegpunkte) |

## 2. Löschkandidaten

Phase 2 löscht nichts direkt: alles wandert zuerst nach `_to_delete/` (mit Ordnerstruktur) und wird erst nach deinem Testlauf endgültig gelöscht.

### SICHER (32.7 MB, 2796 Dateien)

| # | Pfad | Größe | Dateien | Grund |
|---|---|---|---|---|
| S1 | `minecraft/logs/2026-09-30-1.log.gz`, `minecraft/logs/2026-09-30-10.log.gz`, `minecraft/logs/2026-09-30-2.log.gz`, `minecraft/logs/2026-09-30-3.log.gz` … (+44) | 1.1 MB | 48 | Logs: alte Logs; behalten werden latest.log, debug.log und die jeweils neueste gepackte Datei |
| S2 | `minecraft/crash-reports/crash-2026-09-30_20.13.50-fml.txt`, `minecraft/crash-reports/crash-2026-09-30_20.17.13-server.txt` | 41.5 KB | 2 | Crash-Reports: alte Absturzberichte (vom 2026-09-30, vor dem Umbau); der neueste bleibt |
| S3 | `minecraft/config/DistantHorizons.toml` | 37.1 KB | 1 | Reste entfernter Mods: Config von Distant Horizons; die Mod ist nicht mehr installiert (modId 'distanthorizons' in keinem Jar) |
| S4 | `minecraft/config/sophisticatedcore-common.toml` | 3.7 KB | 1 | Reste entfernter Mods: Config von Sophisticated Core (Sophisticated Backpacks); die Mod ist nicht mehr installiert (modId 'sophisticatedcore' in keinem Jar) |
| S5 | `questtools/__pycache__` | 92.6 KB | 6 | Caches: Python-Cache, wird automatisch neu erzeugt |
| S6 | `minecraft/modernfix/structureCacheV1` | 15.7 MB | 503 | Caches: ModernFix-Cache, wird beim nächsten Start neu aufgebaut (erster Start etwas langsamer) |
| S7 | `minecraft/essential/cosmetic-cache` | 15.7 MB | 2235 | Caches: Essential-Kosmetik-Cache, wird bei Bedarf neu geladen |

### WAHRSCHEINLICH (336.0 MB, 1740 Dateien)

| # | Pfad | Größe | Dateien | Grund |
|---|---|---|---|---|
| W1 | `backup/2026-10-09_010902_jade_neat/mods/aether-1.20.1-1.5.2-neoforge.jar`, `backup/2026-10-09_010902_jade_neat/mods/alexsmobs-1.22.9.jar`, `backup/2026-10-09_010902_jade_neat/mods/AmbientSounds_FORGE_v6.3.10_mc1.20.1.jar`, `backup/2026-10-09_010902_jade_neat/mods/appleskin-forge-mc1.20.1-2.5.1.jar` … (+46) | 283.3 MB | 50 | Alte Backups: 50 Mod-Jars in der Sicherung vor Jade/Neat sind byte-gleich (MD5) mit den aktuellen Jars in mods/; Jade/Neat laufen seit dem 2026-10-09 |
| W2 | `minecraft/tacz_backup` | 49.2 MB | 1 | Caches: TaCZ-eigene Sicherung des Standard-Waffenpakets vom 2026-10-06; das Paket liegt entpackt in tacz/ und im TaCZ-Jar |
| W3 | `backup/2026-10-09_001517_elytra_dungeons`, `backup/2026-10-09_002149_elytra_dungeons`, `backup/2026-10-09_003859_elytra_dungeons`, `backup/2026-10-09_005047_elytra_dungeons` … (+18) | 2.1 MB | 1621 | Alte Backups: ältere Stände derselben Sicherungsreihe (elytra_dungeons, Ressourcenpakete, leaders); die jeweils neueste bleibt |
| W4 | `backup/instance.cfg.2026-10-13_005850.bak`, `backup/instance.cfg.2026-10-13_011616.bak` | 3.6 KB | 2 | Alte Backups: Sicherungen von instance.cfg vor dem Pre-Launch-Fix (der Fix läuft) |
| W5 | `questtools/backups` | 781.3 KB | 59 | Skripte: alte Generator-Stände (messengergen_before_*.py usw.); die aktuellen Generatoren ersetzen sie |
| W6 | `questtools/.gamedata_cache.json` | 580.5 KB | 1 | Caches: Index-Cache der Generatoren, wird beim nächsten Lauf neu gebaut (dauert dann ein paar Sekunden) |
| W7 | `questtools/validate_report.txt`, `questtools/balance_report.txt`, `questtools/loot_report.txt`, `mod-check-report.txt` | 32.1 KB | 4 | Skripte: erzeugte Berichte, werden bei jedem Lauf neu geschrieben |
| W8 | `minecraft/XaeroWaypoints_BACKUP240807` | 0.6 KB | 2 | Reste: Xaero-eigene Sicherung alter Wegpunkte (Ordner 'first try'); aktuelle Wegpunkte liegen in xaero/ |

### UNKLAR (1.0 KB, 3 Dateien)

| # | Pfad | Größe | Dateien | Grund |
|---|---|---|---|---|
| U1 | `minecraft/local/ftbquests/saved` | 0.5 KB | 2 | Quest-Dateien: FTB-Quests-Schnappschuss vom 2026-09-30 (chapter_groups/data, fast leer); ob FTB ihn noch nutzt, weiß ich nicht |
| U2 | `exports` | 0.4 KB | 1 | Skripte: Zip des Ressourcenpakets 'Silent Zombie Awareness' zum Weitergeben; brauchst du es noch? |

### Geprüft, aber nichts gefunden

- **Doppelte Mods:** keine Mod-ID kommt in zwei Jars vor; keine `.disabled`-Dateien (55 Jars geprüft).
- **Reste von Torcy:** keine Config, kein Ordner gefunden. Sophisticated Backpacks: nur `sophisticatedcore-common.toml` (S-Liste). Distant Horizons: nur `DistantHorizons.toml` (S-Liste); seine Daten lägen in den Welten (nie anfassen).
- **Quest-Kapitel:** alle 26 Dateien in `chapters/` werden von `questtools/questgen.py` erzeugt (nicht dazugehörig: keine; fehlend: keine). `ammo_depot.snbt` gibt es nicht mehr. Weitere Dateien im Quest-Ordner: keine.
- **Heap-Dumps:** keine.
- `config/cumulus_menus-client.toml` sieht verwaist aus, gehört aber zur Aether-Mod (Cumulus ist in ihr eingebaut): bleibt.

## 3. Zusammenfassungs-Kandidaten

### a) Datapacks: NICHT zusammenlegen (Empfehlung)

| Pack | Namespaces | Größe | Dateien | load/tick-Tag |
|---|---|---|---|---|
| elytra_dungeons | elytra_dungeons, minecraft | 173.9 KB | 129 | load, tick |
| elytra_extras | aether, elytra_extras, minecraft, modpack | 163.1 KB | 304 | load, tick |
| elytra_hordes | elytra_hordes, minecraft, modpack | 97.2 KB | 123 | load, tick |
| elytra_rs_trim | repurposed_structures | 1.5 KB | 35 | - |

Gewinn praktisch null (Paxi lädt alle Packs gleich schnell), Risiken:
- Mehrere Packs haben eigene `minecraft/tags/functions/load.json`/`tick.json`; beim Zusammenlegen müssen die Listen von Hand vereinigt werden, sonst läuft z. B. die Horde oder der Bote nicht mehr.
- `elytra_extras` und `elytra_hordes` teilen den Namespace `modpack`; ein Fehler beim Mischen überschreibt Funktionen still.
- Die Generatoren (dungeongen, leadergen, messengergen, rankgen, pathgen) schreiben in feste Pack-Ordner und leeren dort Unterordner; nach dem Zusammenlegen würde der nächste Generator-Lauf das andere Pack beschädigen.
- `config/paxi/datapack_load_order.json` nennt die Packs mit Namen.

### b) Backups in ein Archiv

- `backup/` enthält 37 Einträge. 3490 Dateien sind inhaltsgleiche Kopien anderer Backup-Dateien (4.3 MB).
- Vorschlag: alle Backups vor heute (2026-10-14), die nicht ohnehin auf der Löschliste stehen, in **ein** Archiv `backup/archive-bis-2026-10-14.zip`: 1053 Dateien, 2.8 MB roh, **gezippt 1.7 MB** (gemessen). Die heutigen Sicherungen (bote-*, ranks-*, pfadbelohnungen-*) bleiben offen liegen.
- Hinweis: dungeongen, leadergen und configure_hud legen bei jedem Lauf neue Ordner in `backup/` an; das Archiv ersetzt also nur den Altbestand.

### c) Notizen und Skripte ordnen

Vorschlag (nur Verschieben, kein Inhalt wird geändert):
| jetzt | neu | Hinweis |
|---|---|---|
| CHANGELOG.md, PROJECT_SUMMARY.md, BRIEFING_FOR_CLAUDE_CHAT.md, COMMANDS.txt, STATUS.md | docs/ | README.md bleibt oben (GitHub-Startseite) |
| devnotes/ | docs/devnotes/ | |
| cleanup/ | docs/cleanup/ | erst nach Phase 2 |
| audit/ | **bleibt** | `audit_quests.py` findet die Instanz über seinen eigenen Ordner; verschoben würde es falsch rechnen (Pfad-Änderung = Inhaltsänderung) |
| questtools/ | **bleibt** | der Pre-Launch-Befehl in `instance.cfg` zeigt auf `questtools/prelaunch.cmd` |
| check-mods.ps1 | **bleibt** | ohne genaue Prüfung seiner Pfade nicht verschieben |

## 4. Nie anfassen

- `minecraft/saves/` (Welten, Spielstände, auch Distant-Horizons-Daten darin), `minecraft/screenshots/`, `essential/screenshot-*`
- `minecraft/options.txt`, `servers.dat`, `ops.json`, `whitelist.json`, `usercache.json`, `usernamecache.json`
- Quest-Fortschritt (in den Welten) und `minecraft/local/ftbquests/client-config.snbt`, `minecraft/local/ftblibrary-client.snbt`
- `minecraft/xaero/` (Kartendaten und Wegpunkte des Spielers)
- `minecraft/mods/` (inkl. `.index` von Prism) - nichts doppelt oder deaktiviert gefunden
- `minecraft/config/` außer den zwei S-Kandidaten; alle Datapacks und Ressourcenpakete
- `minecraft/tacz/` (Standard-Waffenpaket und `elytra_loot`), `minecraft/essential/` außer dem Kosmetik-Cache
- alles außerhalb von `minecraft/` der Prism-Instanz: `instance.cfg`, `mmc-pack.json`, `patches/`, `.packignore`, `elytra_pack_icon.png`, `questtools/` (außer den S/W-Punkten), `audit/`, `README.md`

Achtung, Widerspruch in der Aufgabe: `backup/`, `questtools/`, die Notizen und `exports/` liegen **außerhalb** von `minecraft/`. Ich führe dort nur Punkte aus, die du ausdrücklich freigibst.

## 5. Erwarteter Gewinn

| Stufe | frei | Dateien weniger | Instanz danach |
|---|---|---|---|
| heute | - | - | 2.39 GB, 13664 Dateien |
| nur SICHER | 32.7 MB | 2796 | 2.36 GB, 10868 Dateien |
| SICHER + WAHRSCHEINLICH | 368.7 MB | 4536 | 2.03 GB, 9128 Dateien |
| + Backup-Archiv (3b) | 1.1 MB weitere | 1052 weitere | 2.03 GB, 8076 Dateien |

UNKLAR-Punkte zusammen: 1.0 KB (nicht eingerechnet). Die Sicherung vor dem Aufräumen (`backup/cleanup-<Zeit>.zip`) kostet vorübergehend zusätzlichen Platz, bis du sie löschst.

## 6. Risiken

- **Jade/Neat-Sicherung (W):** danach gibt es keine zweite Kopie der Mod-Jars mehr außerhalb von `mods/`. Die Jars lassen sich aber neu herunterladen; die Versionen stehen in `mods/.index`.
- **ModernFix-/Essential-Cache (S):** der erste Spielstart danach dauert etwas länger; Essential lädt Kosmetik neu (Internet nötig).
- **TaCZ-Sicherung (W):** falls das Standard-Waffenpaket in `tacz/` kaputtgeht, gibt es keine lokale Kopie mehr; TaCZ entpackt es aber aus seinem Jar neu.
- **Alte Backup-Reihen (W):** Zwischenstände der Boss-Dungeons und Leader vom 2026-10-09 wären weg (die jeweils neueste bleibt).
- **questtools/backups (W):** alte Generator-Versionen; nützlich nur, wenn du zu einem sehr alten Bote-Stand zurück willst.
- **Gamedata-Cache (W):** wird neu gebaut; der Pre-Launch-Validator braucht dafür beim ersten Start ein paar Sekunden mehr.
- **Verschieben der Notizen (3c):** Verweise auf `STATUS.md`/`CHANGELOG.md` in meinen Notizen und im Briefing zeigen danach auf den alten Ort.
- **Prism-Export:** `.packignore` schließt nur `minecraft/saves` aus - ein Export enthält heute also auch `backup/` (290 MB), `questtools/`, `audit/`. Das ist ein Grund mehr, `backup/` klein zu halten; `.packignore` selbst ändere ich nicht ohne dein OK.

## Laufende Änderungen
Die letzten Änderungen in der Instanz (Datapacks, STATUS.md) stammen aus dieser Sitzung (Pfad-Belohnungen, ca. 03:07). Eine andere Sitzung, die gerade Dateien ändert, habe ich nicht gefunden. Vor Phase 2 prüfe ich das erneut.
