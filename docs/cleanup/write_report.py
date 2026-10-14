"""Writes docs/cleanup/CLEANUP_REPORT.md from _to_delete/MANIFEST.json and fresh measurements (read only otherwise)."""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = HERE
while not os.path.exists(os.path.join(INST, "instance.cfg")):
    INST = os.path.dirname(INST)
TD = os.path.join(INST, "_to_delete")
man = json.load(open(os.path.join(TD, "MANIFEST.json"), encoding="utf-8"))


def sc(p):
    if os.path.isfile(p):
        return os.path.getsize(p), 1
    s = n = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            s += os.path.getsize(os.path.join(r, f))
            n += 1
    return s, n


def fmt(b):
    return f"{b / 1024 ** 3:.2f} GB" if b >= 1024 ** 3 else f"{b / 1024 ** 2:.1f} MB" if b >= 1024 ** 2 else f"{b / 1024:.1f} KB"


tot = sc(INST)
td = sc(TD)
safety = sc(os.path.join(INST, man["safety_zip"]))
arch = sc(os.path.join(INST, man["archive_zip"]))
game = (tot[0] - td[0] - safety[0], tot[1] - td[1] - safety[1])
BEFORE = (2.39 * 1024 ** 3, 13664)    # from CLEANUP_PLAN.md (measured 2026-10-14 03:12)
groups = {}
for m in man["moved"]:
    if m["to"].startswith("docs/"):
        k = "nach docs/ verschoben"
    elif m["from"].startswith("backup/") and "jade_neat/mods" not in m["from"]:
        k = "alte Backups (nach _to_delete/, Inhalt im Archiv oder W3/W4)"
    else:
        k = "Lösch-Kandidaten S/W/U (nach _to_delete/)"
    groups.setdefault(k, []).append(m)
o = []
P = o.append
P("# Aufräum-Bericht (Phase 2)\n")
P(f"Ausgeführt am {man['created'][:10]} um {man['created'][11:13]}:{man['created'][13:15]}, freigegeben: alle S-, W- und U-Punkte, "
  "Backup-Archiv, Ordnung in docs/. Endgültig gelöscht wurde **nichts**.\n")
P("## Was passiert ist\n")
P(f"1. **Sicherung:** `{man['safety_zip']}`. Sie enthält alle {safety[1] and ''}verschobenen Dateien und wurde geprüft: "
  "lesbar, gleiche Dateianzahl, gleiche Bytes.")
P(f"2. **Verschoben nach `_to_delete/`** (mit Originalstruktur): {len(groups.get('Lösch-Kandidaten S/W/U (nach _to_delete/)', []))} Pfade "
  "(S1–S7, W1–W8, U1–U2 aus `CLEANUP_PLAN.md`).")
P(f"3. **Backup-Archiv:** `{man['archive_zip']}` ({fmt(arch[0])}) enthält den Altbestand von 9 Sicherungen "
  "(neueste Stände der Reihen + Einzelsicherungen). Geprüft, Originale nach `_to_delete/backup/`.")
P("4. **Ordnung:** `CHANGELOG.md`, `PROJECT_SUMMARY.md`, `BRIEFING_FOR_CLAUDE_CHAT.md`, `COMMANDS.txt`, `STATUS.md`, `devnotes/` "
  "und `cleanup/` liegen jetzt in `docs/`. Pfadangaben in `README.md` und `docs/COMMANDS.txt` angepasst; "
  "die Aufräum-Skripte finden die Instanz jetzt selbst. `questtools/` und `audit/` bleiben (Pre-Launch-Befehl, Audit-Pfade).")
P("5. **Nicht angefasst:** Datapacks (nicht zusammengelegt), Mods, Configs außer S3/S4, Welten, Screenshots, Prism-Dateien, `.packignore`.\n")
P("## Platz\n")
P("| | Größe | Dateien |\n|---|---|---|")
P(f"| vorher (Plan) | {fmt(BEFORE[0])} | {BEFORE[1]} |")
P(f"| jetzt ohne `_to_delete/` und ohne Sicherungs-Zip | **{fmt(game[0])}** | **{game[1]}** |")
P(f"| `_to_delete/` (wartet auf deine Bestätigung) | {fmt(td[0])} | {td[1]} |")
P(f"| Sicherungs-Zip | {fmt(safety[0])} | 1 |")
P(f"| jetzt insgesamt auf der Platte | {fmt(tot[0])} | {tot[1]} |")
P(f"\nNach dem endgültigen Löschen von `_to_delete/` und der Sicherung werden **{fmt(BEFORE[0] - game[0])}** frei "
  "(bis dahin belegt die Sicherung den Platz doppelt).\n")
P("## Prüfungen danach\n")
P("- `questtools/validate.py`: 26 Kapitel, 299 Quests, alle SNBT gültig, IDs eindeutig, alle JSON/mcfunction-Prüfungen ohne Fehler (0 Fehler, 0 Warnungen).")
P("- Kein Verweis in `questtools/`, `audit/`, `minecraft/config/` (inkl. aller Datapacks), `instance.cfg`, `README.md`, `.packignore` "
  "zeigt auf eine verschobene Datei. Der Gamedata-Cache und `questtools/backups/` werden von den Werkzeugen selbst neu angelegt.")
P("- Alte Pfade nur noch in historischen CHANGELOG-Einträgen (Absicht: das ist Geschichte).\n")
P("## Rückgängig machen\n")
P("- **Alles:** jeden Eintrag aus `_to_delete/MANIFEST.json` zurückschieben (`to` -> `from`), dann `docs/`-Dateien an die alten Orte, "
  "und die zwei Pfadzeilen in `README.md` zurück. Oder einfach `" + man["safety_zip"] + "` im Instanzordner entpacken "
  "(alle Pfade im Zip sind relativ zum Instanzordner).")
P("- **Einzelne Datei:** aus `_to_delete/<alter Pfad>` an `<alter Pfad>` zurücklegen.")
P("- **Archiv:** `backup/archive-bis-2026-10-14.zip` in `backup/` entpacken.\n")
P("## Was noch fehlt\n")
P("- Dein Testlauf (Welt laden, Quest-Buch, Bote-Szene, Horde). Danach sage ich `_to_delete/` und ggf. das Sicherungs-Zip endgültig weg.")
P("- Offen: `.packignore` um `backup/` erweitern (ein Prism-Export nimmt `backup/` sonst mit).\n")
P("## Alle Verschiebungen\n")
for k, ms in groups.items():
    P(f"### {k} ({len(ms)})\n")
    for m in ms:
        P(f"- `{m['from']}` -> `{m['to']}`")
    P("")
with open(os.path.join(HERE, "CLEANUP_REPORT.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(o) + "\n")
print(f"now {fmt(game[0])} / {game[1]} files; _to_delete {fmt(td[0])}/{td[1]}; safety {fmt(safety[0])}; freed {fmt(BEFORE[0] - game[0])}")
