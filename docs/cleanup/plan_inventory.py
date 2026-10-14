"""Cleanup plan (phase 1, READ ONLY): measures the instance and writes cleanup/CLEANUP_PLAN.md.
Nothing is moved, changed or deleted. Usage: py cleanup/plan_inventory.py"""

import hashlib
import io
import os
import re
import time
import zipfile
from collections import defaultdict

CLEAN = os.path.dirname(os.path.abspath(__file__))
INST = CLEAN
while not os.path.exists(os.path.join(INST, "instance.cfg")):     # the instance folder (works from cleanup/ or docs/cleanup/)
    INST = os.path.dirname(INST)
MC = os.path.join(INST, "minecraft")
BK = os.path.join(INST, "backup")


def walk_files(p):
    if os.path.isfile(p):
        yield p
        return
    for root, _, files in os.walk(p):
        for f in files:
            yield os.path.join(root, f)


def size_count(p):
    s = n = 0
    for f in walk_files(p):
        try:
            s += os.path.getsize(f)
            n += 1
        except OSError:
            pass
    return s, n


def fmt(b):
    if b >= 1024 ** 3:
        return f"{b / 1024 ** 3:.2f} GB"
    if b >= 1024 ** 2:
        return f"{b / 1024 ** 2:.1f} MB"
    return f"{b / 1024:.1f} KB"


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, INST).replace("\\", "/")


# ------------------------------------------------------------------ overview
DESCR = {
    "minecraft": "das Spiel (Prism-Ordner .minecraft)", "backup": "unsere Sicherungen (von Hand und von den Generatoren)",
    "questtools": "Generatoren und Prüfer (Quests, Datapacks, Validator; Pre-Launch-Befehl zeigt hierher)",
    "audit": "Quest-Audit (Bericht + Skripte)", "cleanup": "dieser Plan", "devnotes": "Phasen-Notizen der Boss-Dungeons",
    "exports": "exportierte Ressourcenpaket-Zips", "saves": "Welten (Spielstände)", "mods": "Mod-Jars (+ .index von Prism)",
    "config": "Mod-Einstellungen, Quests, Paxi-Datapacks", "logs": "Spiel-Logs", "crash-reports": "Absturzberichte",
    "essential": "Essential-Mod: Loader, Bibliotheken, Caches", "modernfix": "ModernFix-Cache (Strukturen)",
    "tacz": "TaCZ-Waffenpakete (Standardpaket + elytra_loot)", "tacz_backup": "automatische Sicherung des TaCZ-Standardpakets",
    "xaero": "Xaero Minimap/Weltkarte (Kartendaten, Wegpunkte)", "screenshots": "Screenshots des Spielers",
    "resourcepacks": "Ressourcenpakete", "local": "lokale FTB-Einstellungen", "defaultconfigs": "Standard-Configs für neue Welten",
    "XaeroWaypoints_BACKUP240807": "Xaero-eigene Sicherung alter Wegpunkte",
}
overview = []
for top in sorted(os.listdir(INST)):
    p = os.path.join(INST, top)
    s, n = size_count(p)
    overview.append((top, s, n, os.path.isdir(p)))
mc_over = []
for top in sorted(os.listdir(MC)):
    p = os.path.join(MC, top)
    s, n = size_count(p)
    mc_over.append((top, s, n, os.path.isdir(p)))
TOTAL = size_count(INST)

# ------------------------------------------------------------------ candidates
cands = []   # (level, path list, reason, group)


def add(level, paths, reason, group):
    paths = [p for p in paths if os.path.exists(p)]
    if paths:
        cands.append((level, paths, reason, group))


# logs: keep latest.log, debug.log and the newest rotated file of each kind
logs = os.path.join(MC, "logs")
lf = [os.path.join(logs, f) for f in os.listdir(logs)] if os.path.isdir(logs) else []
keep = {os.path.join(logs, "latest.log"), os.path.join(logs, "debug.log")}
for pat in (r"^\d{4}-\d\d-\d\d-\d+\.log\.gz$", r"^debug-\d+\.log\.gz$"):
    g = [f for f in lf if re.match(pat, os.path.basename(f))]
    if g:
        keep.add(max(g, key=os.path.getmtime))
add("SICHER", [f for f in lf if f not in keep and os.path.isfile(f)],
    "alte Logs; behalten werden latest.log, debug.log und die jeweils neueste gepackte Datei", "Logs")
cr = os.path.join(MC, "crash-reports")
crf = sorted((os.path.join(cr, f) for f in os.listdir(cr)), key=os.path.getmtime) if os.path.isdir(cr) else []
add("SICHER", crf[:-1], "alte Absturzberichte (vom 2026-09-30, vor dem Umbau); der neueste bleibt", "Crash-Reports")
heaps = [f for f in walk_files(INST) if "saves" not in f.split(os.sep)
         and (f.endswith((".hprof", ".mdmp")) or os.path.basename(f).startswith("hs_err_pid"))]
add("SICHER", heaps, "Heap-Dumps / JVM-Absturzdateien", "Heap-Dumps")

# configs of mods that are no longer installed (mod ids read from every jar incl. jar-in-jar)
def jar_ids(data):
    ids = set()
    z = zipfile.ZipFile(io.BytesIO(data))
    names = z.namelist()
    if "META-INF/mods.toml" in names:
        t = z.read("META-INF/mods.toml").decode("utf-8", "ignore")
        for block in re.split(r"^\s*\[\[", t, flags=re.M):
            if block.startswith("mods]]"):
                ids |= set(re.findall(r'^\s*modId\s*=\s*"([^"]+)"', block, re.M))
    for n in names:
        if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
            try:
                ids |= jar_ids(z.read(n))
            except zipfile.BadZipFile:
                pass
    return ids


modids = set()
jars = [f for f in os.listdir(os.path.join(MC, "mods")) if f.endswith(".jar")]
for f in jars:
    modids |= jar_ids(open(os.path.join(MC, "mods", f), "rb").read())
REMOVED = {"DistantHorizons.toml": ("distanthorizons", "Distant Horizons"),
           "sophisticatedcore-common.toml": ("sophisticatedcore", "Sophisticated Core (Sophisticated Backpacks)")}
for f, (mid, name) in REMOVED.items():
    if mid not in modids:
        add("SICHER", [os.path.join(MC, "config", f)], f"Config von {name}; die Mod ist nicht mehr installiert "
                                                         f"(modId '{mid}' in keinem Jar)", "Reste entfernter Mods")
disabled = [os.path.join(MC, "mods", f) for f in os.listdir(os.path.join(MC, "mods")) if f.endswith(".disabled")]
add("SICHER", disabled, "deaktivierte Mod-Jars", "Doppelte/deaktivierte Jars")

add("SICHER", [os.path.join(INST, "questtools", "__pycache__")], "Python-Cache, wird automatisch neu erzeugt", "Caches")
add("SICHER", [os.path.join(MC, "modernfix", "structureCacheV1")],
    "ModernFix-Cache, wird beim nächsten Start neu aufgebaut (erster Start etwas langsamer)", "Caches")
add("SICHER", [os.path.join(MC, "essential", "cosmetic-cache")],
    "Essential-Kosmetik-Cache, wird bei Bedarf neu geladen", "Caches")

# jade_neat backup: mods identical to the current mods/
jn = os.path.join(BK, "2026-10-09_010902_jade_neat", "mods")
same, differ = [], []
if os.path.isdir(jn):
    for f in os.listdir(jn):
        a, b = os.path.join(jn, f), os.path.join(MC, "mods", f)
        if os.path.isfile(a) and os.path.isfile(b) and md5(a) == md5(b):
            same.append(a)
        elif os.path.isfile(a):
            differ.append(a)
add("WAHRSCHEINLICH", same, f"{len(same)} Mod-Jars in der Sicherung vor Jade/Neat sind byte-gleich (MD5) mit den "
                            f"aktuellen Jars in mods/; Jade/Neat laufen seit dem 2026-10-09", "Alte Backups")
if differ:
    add("UNKLAR", differ, "Dateien in der Jade/Neat-Sicherung, die es in mods/ nicht (gleich) gibt", "Alte Backups")
add("WAHRSCHEINLICH", [os.path.join(MC, "tacz_backup")],
    "TaCZ-eigene Sicherung des Standard-Waffenpakets vom 2026-10-06; das Paket liegt entpackt in tacz/ und im TaCZ-Jar",
    "Caches")

# backup series: keep the newest of each series
series = defaultdict(list)
for b in os.listdir(BK):
    m = re.match(r"^(\d{4}-\d\d-\d\d_\d{6})_(.+)$", b) or re.match(r"^(.+?)-(\d{4}-\d\d-\d\d_\d{6})$", b)
    if not m:
        continue
    name = m.group(2) if b[0].isdigit() else m.group(1)
    series[name].append(os.path.join(BK, b))
old_series = []
for name, lst in series.items():
    if len(lst) > 1:
        lst.sort(key=lambda p: os.path.basename(p))
        old_series += lst[:-1]
add("WAHRSCHEINLICH", sorted(old_series), "ältere Stände derselben Sicherungsreihe (elytra_dungeons, Ressourcenpakete, "
                                          "leaders); die jeweils neueste bleibt", "Alte Backups")
add("WAHRSCHEINLICH", [os.path.join(BK, f) for f in os.listdir(BK) if f.startswith("instance.cfg.")],
    "Sicherungen von instance.cfg vor dem Pre-Launch-Fix (der Fix läuft)", "Alte Backups")
add("WAHRSCHEINLICH", [os.path.join(INST, "questtools", "backups")],
    "alte Generator-Stände (messengergen_before_*.py usw.); die aktuellen Generatoren ersetzen sie", "Skripte")
add("WAHRSCHEINLICH", [os.path.join(INST, "questtools", ".gamedata_cache.json")],
    "Index-Cache der Generatoren, wird beim nächsten Lauf neu gebaut (dauert dann ein paar Sekunden)", "Caches")
add("WAHRSCHEINLICH", [os.path.join(INST, "questtools", f) for f in ("validate_report.txt", "balance_report.txt",
                                                                     "loot_report.txt")]
    + [os.path.join(INST, "mod-check-report.txt")],
    "erzeugte Berichte, werden bei jedem Lauf neu geschrieben", "Skripte")
add("WAHRSCHEINLICH", [os.path.join(MC, "XaeroWaypoints_BACKUP240807")],
    "Xaero-eigene Sicherung alter Wegpunkte (Ordner 'first try'); aktuelle Wegpunkte liegen in xaero/", "Reste")
add("UNKLAR", [os.path.join(MC, "local", "ftbquests", "saved")],
    "FTB-Quests-Schnappschuss vom 2026-09-30 (chapter_groups/data, fast leer); ob FTB ihn noch nutzt, weiß ich nicht",
    "Quest-Dateien")
add("UNKLAR", [os.path.join(INST, "exports")], "Zip des Ressourcenpakets 'Silent Zombie Awareness' zum Weitergeben; "
                                             "brauchst du es noch?", "Skripte")

# ------------------------------------------------------------------ quests
qdir = os.path.join(MC, "config", "ftbquests", "quests")
qgen = open(os.path.join(INST, "questtools", "questgen.py"), encoding="utf-8").read()
gen_chapters = set(re.findall(r"Chapter\('([a-z0-9_]+)'", qgen))
chap_files = sorted(f[:-5] for f in os.listdir(os.path.join(qdir, "chapters")) if f.endswith(".snbt"))
orphan_chapters = [c for c in chap_files if c not in gen_chapters]
missing_chapters = [c for c in gen_chapters if c not in chap_files]
other_q = sorted(rel(f) for f in walk_files(qdir) if not f.endswith(".snbt"))

# ------------------------------------------------------------------ backups as one archive (measured, in memory)
today = time.strftime("%Y-%m-%d")
cand_paths = {os.path.normpath(p) for _, ps, _, _ in cands for p in ps}
arch_src = []
for b in sorted(os.listdir(BK)):
    p = os.path.join(BK, b)
    if today in b or b.startswith(f"bote-") or b.startswith(("ranks-", "pfadbelohnungen-")):
        continue
    for f in walk_files(p):
        if not any(os.path.normpath(f).startswith(c) for c in cand_paths):
            arch_src.append(f)
raw = sum(os.path.getsize(f) for f in arch_src)
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    for f in arch_src:
        z.write(f, rel(f))
zipped = buf.tell()
hashes = defaultdict(list)
for f in walk_files(BK):
    hashes[md5(f)].append(f)
dup_files = sum(len(v) - 1 for v in hashes.values() if len(v) > 1)
dup_bytes = sum(os.path.getsize(v[0]) * (len(v) - 1) for v in hashes.values() if len(v) > 1)

# ------------------------------------------------------------------ datapacks
paxi = os.path.join(MC, "config", "paxi", "datapacks")
packs = []
for pk in sorted(os.listdir(paxi)):
    d = os.path.join(paxi, pk, "data")
    ns = sorted(os.listdir(d)) if os.path.isdir(d) else []
    s, n = size_count(os.path.join(paxi, pk))
    tags = [t for t in ("load", "tick") if os.path.exists(os.path.join(d, "minecraft", "tags", "functions", f"{t}.json"))]
    packs.append((pk, ns, s, n, tags))

# ------------------------------------------------------------------ write the plan
def total_of(level):
    s = n = 0
    for lv, ps, _, _ in cands:
        if lv == level:
            for p in ps:
                a, b = size_count(p)
                s += a
                n += b
    return s, n


o = []
P = o.append
s_s, s_n = total_of("SICHER")
w_s, w_n = total_of("WAHRSCHEINLICH")
u_s, u_n = total_of("UNKLAR")
P("# Aufräum-Plan (Phase 1: nur Bestandsaufnahme, es wurde NICHTS geändert)\n")
P(f"Erzeugt von `cleanup/plan_inventory.py` am {time.strftime('%Y-%m-%d %H:%M')}. Alle Größen sind gemessen.\n")
P("## 1. Übersicht\n")
P(f"Instanz gesamt: **{fmt(TOTAL[0])}**, {TOTAL[1]} Dateien.\n")
P("| Instanzordner | Größe | Dateien | Zweck |\n|---|---|---|---|")
for top, s, n, isd in overview:
    P(f"| {top}{'/' if isd else ''} | {fmt(s)} | {n} | {DESCR.get(top, '')} |")
P("\n| minecraft/… | Größe | Dateien | Zweck |\n|---|---|---|---|")
for top, s, n, isd in mc_over:
    P(f"| {top}{'/' if isd else ''} | {fmt(s)} | {n} | {DESCR.get(top, '')} |")
P("\n## 2. Löschkandidaten\n")
P("Phase 2 löscht nichts direkt: alles wandert zuerst nach `_to_delete/` (mit Ordnerstruktur) und wird erst nach "
  "deinem Testlauf endgültig gelöscht.\n")
for level in ("SICHER", "WAHRSCHEINLICH", "UNKLAR"):
    s, n = total_of(level)
    P(f"### {level} ({fmt(s)}, {n} Dateien)\n")
    P("| # | Pfad | Größe | Dateien | Grund |\n|---|---|---|---|---|")
    k = 0
    for lv, ps, reason, group in cands:
        if lv != level:
            continue
        k += 1
        tot_s = sum(size_count(p)[0] for p in ps)
        tot_n = sum(size_count(p)[1] for p in ps)
        shown = ", ".join(f"`{rel(p)}`" for p in ps[:4]) + (f" … (+{len(ps) - 4})" if len(ps) > 4 else "")
        P(f"| {level[0]}{k} | {shown} | {fmt(tot_s)} | {tot_n} | {group}: {reason} |")
    P("")
P("### Geprüft, aber nichts gefunden\n")
P(f"- **Doppelte Mods:** keine Mod-ID kommt in zwei Jars vor; keine `.disabled`-Dateien ({len(jars)} Jars geprüft).")
P("- **Reste von Torcy:** keine Config, kein Ordner gefunden. Sophisticated Backpacks: nur `sophisticatedcore-common.toml` (S-Liste). "
  "Distant Horizons: nur `DistantHorizons.toml` (S-Liste); seine Daten lägen in den Welten (nie anfassen).")
P(f"- **Quest-Kapitel:** alle {len(chap_files)} Dateien in `chapters/` werden von `questtools/questgen.py` erzeugt "
  f"(nicht dazugehörig: {orphan_chapters or 'keine'}; fehlend: {missing_chapters or 'keine'}). `ammo_depot.snbt` gibt es nicht mehr. "
  f"Weitere Dateien im Quest-Ordner: {other_q or 'keine'}.")
P("- **Heap-Dumps:** keine.")
P("- `config/cumulus_menus-client.toml` sieht verwaist aus, gehört aber zur Aether-Mod (Cumulus ist in ihr eingebaut): bleibt.")
P("")
P("## 3. Zusammenfassungs-Kandidaten\n")
P("### a) Datapacks: NICHT zusammenlegen (Empfehlung)\n")
P("| Pack | Namespaces | Größe | Dateien | load/tick-Tag |\n|---|---|---|---|---|")
for pk, ns, s, n, tags in packs:
    P(f"| {pk} | {', '.join(ns)} | {fmt(s)} | {n} | {', '.join(tags) or '-'} |")
P("\nGewinn praktisch null (Paxi lädt alle Packs gleich schnell), Risiken:")
P("- Mehrere Packs haben eigene `minecraft/tags/functions/load.json`/`tick.json`; beim Zusammenlegen müssen die Listen von Hand vereinigt werden, sonst läuft z. B. die Horde oder der Bote nicht mehr.")
P("- `elytra_extras` und `elytra_hordes` teilen den Namespace `modpack`; ein Fehler beim Mischen überschreibt Funktionen still.")
P("- Die Generatoren (dungeongen, leadergen, messengergen, rankgen, pathgen) schreiben in feste Pack-Ordner und leeren dort Unterordner; nach dem Zusammenlegen würde der nächste Generator-Lauf das andere Pack beschädigen.")
P("- `config/paxi/datapack_load_order.json` nennt die Packs mit Namen.")
P("")
P("### b) Backups in ein Archiv\n")
P(f"- `backup/` enthält {len(os.listdir(BK))} Einträge. {dup_files} Dateien sind inhaltsgleiche Kopien anderer Backup-Dateien ({fmt(dup_bytes)}).")
P(f"- Vorschlag: alle Backups vor heute ({today}), die nicht ohnehin auf der Löschliste stehen, in **ein** Archiv "
  f"`backup/archive-bis-{today}.zip`: {len(arch_src)} Dateien, {fmt(raw)} roh, **gezippt {fmt(zipped)}** (gemessen). "
  "Die heutigen Sicherungen (bote-*, ranks-*, pfadbelohnungen-*) bleiben offen liegen.")
P("- Hinweis: dungeongen, leadergen und configure_hud legen bei jedem Lauf neue Ordner in `backup/` an; das Archiv ersetzt also nur den Altbestand.")
P("")
P("### c) Notizen und Skripte ordnen\n")
P("Vorschlag (nur Verschieben, kein Inhalt wird geändert):")
P("| jetzt | neu | Hinweis |\n|---|---|---|")
P("| CHANGELOG.md, PROJECT_SUMMARY.md, BRIEFING_FOR_CLAUDE_CHAT.md, COMMANDS.txt, STATUS.md | docs/ | README.md bleibt oben (GitHub-Startseite) |")
P("| devnotes/ | docs/devnotes/ | |")
P("| cleanup/ | docs/cleanup/ | erst nach Phase 2 |")
P("| audit/ | **bleibt** | `audit_quests.py` findet die Instanz über seinen eigenen Ordner; verschoben würde es falsch rechnen (Pfad-Änderung = Inhaltsänderung) |")
P("| questtools/ | **bleibt** | der Pre-Launch-Befehl in `instance.cfg` zeigt auf `questtools/prelaunch.cmd` |")
P("| check-mods.ps1 | **bleibt** | ohne genaue Prüfung seiner Pfade nicht verschieben |")
P("")
P("## 4. Nie anfassen\n")
for line in [
    "`minecraft/saves/` (Welten, Spielstände, auch Distant-Horizons-Daten darin), `minecraft/screenshots/`, `essential/screenshot-*`",
    "`minecraft/options.txt`, `servers.dat`, `ops.json`, `whitelist.json`, `usercache.json`, `usernamecache.json`",
    "Quest-Fortschritt (in den Welten) und `minecraft/local/ftbquests/client-config.snbt`, `minecraft/local/ftblibrary-client.snbt`",
    "`minecraft/xaero/` (Kartendaten und Wegpunkte des Spielers)",
    "`minecraft/mods/` (inkl. `.index` von Prism) - nichts doppelt oder deaktiviert gefunden",
    "`minecraft/config/` außer den zwei S-Kandidaten; alle Datapacks und Ressourcenpakete",
    "`minecraft/tacz/` (Standard-Waffenpaket und `elytra_loot`), `minecraft/essential/` außer dem Kosmetik-Cache",
    "alles außerhalb von `minecraft/` der Prism-Instanz: `instance.cfg`, `mmc-pack.json`, `patches/`, `.packignore`, `elytra_pack_icon.png`, "
    "`questtools/` (außer den S/W-Punkten), `audit/`, `README.md`",
]:
    P(f"- {line}")
P("")
P("Achtung, Widerspruch in der Aufgabe: `backup/`, `questtools/`, die Notizen und `exports/` liegen **außerhalb** von `minecraft/`. "
  "Ich führe dort nur Punkte aus, die du ausdrücklich freigibst.")
P("")
P("## 5. Erwarteter Gewinn\n")
after_s = TOTAL[0] - s_s - w_s
after_n = TOTAL[1] - s_n - w_n
P("| Stufe | frei | Dateien weniger | Instanz danach |\n|---|---|---|---|")
P(f"| heute | - | - | {fmt(TOTAL[0])}, {TOTAL[1]} Dateien |")
P(f"| nur SICHER | {fmt(s_s)} | {s_n} | {fmt(TOTAL[0] - s_s)}, {TOTAL[1] - s_n} Dateien |")
P(f"| SICHER + WAHRSCHEINLICH | {fmt(s_s + w_s)} | {s_n + w_n} | {fmt(after_s)}, {after_n} Dateien |")
P(f"| + Backup-Archiv (3b) | {fmt(raw - zipped)} weitere | {len(arch_src) - 1} weitere | {fmt(after_s - raw + zipped)}, {after_n - len(arch_src) + 1} Dateien |")
P(f"\nUNKLAR-Punkte zusammen: {fmt(u_s)} (nicht eingerechnet). Die Sicherung vor dem Aufräumen (`backup/cleanup-<Zeit>.zip`) "
  "kostet vorübergehend zusätzlichen Platz, bis du sie löschst.")
P("")
P("## 6. Risiken\n")
for line in [
    "**Jade/Neat-Sicherung (W):** danach gibt es keine zweite Kopie der Mod-Jars mehr außerhalb von `mods/`. Die Jars lassen sich aber neu herunterladen; die Versionen stehen in `mods/.index`.",
    "**ModernFix-/Essential-Cache (S):** der erste Spielstart danach dauert etwas länger; Essential lädt Kosmetik neu (Internet nötig).",
    "**TaCZ-Sicherung (W):** falls das Standard-Waffenpaket in `tacz/` kaputtgeht, gibt es keine lokale Kopie mehr; TaCZ entpackt es aber aus seinem Jar neu.",
    "**Alte Backup-Reihen (W):** Zwischenstände der Boss-Dungeons und Leader vom 2026-10-09 wären weg (die jeweils neueste bleibt).",
    "**questtools/backups (W):** alte Generator-Versionen; nützlich nur, wenn du zu einem sehr alten Bote-Stand zurück willst.",
    "**Gamedata-Cache (W):** wird neu gebaut; der Pre-Launch-Validator braucht dafür beim ersten Start ein paar Sekunden mehr.",
    "**Verschieben der Notizen (3c):** Verweise auf `STATUS.md`/`CHANGELOG.md` in meinen Notizen und im Briefing zeigen danach auf den alten Ort.",
    "**Prism-Export:** `.packignore` schließt nur `minecraft/saves` aus - ein Export enthält heute also auch `backup/` (290 MB), `questtools/`, `audit/`. "
    "Das ist ein Grund mehr, `backup/` klein zu halten; `.packignore` selbst ändere ich nicht ohne dein OK.",
]:
    P(f"- {line}")
P("")
P("## Laufende Änderungen")
P("Die letzten Änderungen in der Instanz (Datapacks, STATUS.md) stammen aus dieser Sitzung (Pfad-Belohnungen, ca. 03:07). "
  "Eine andere Sitzung, die gerade Dateien ändert, habe ich nicht gefunden. Vor Phase 2 prüfe ich das erneut.")
with open(os.path.join(CLEAN, "CLEANUP_PLAN.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(o) + "\n")
print(f"SICHER {fmt(s_s)}/{s_n}  WAHRSCHEINLICH {fmt(w_s)}/{w_n}  UNKLAR {fmt(u_s)}/{u_n}  archive {fmt(raw)}->{fmt(zipped)} "
      f"({len(arch_src)} files)  total {fmt(TOTAL[0])}/{TOTAL[1]}")
