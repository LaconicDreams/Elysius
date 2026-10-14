"""Cleanup phase 2 (approved: all S, W, U points, backup archive, docs/ structure).
1. full safety zip backup/cleanup-<time>.zip of everything that is moved (checked: readable, same files and sizes)
2. S/W/U candidates -> _to_delete/<original path>   (nothing is deleted)
3. old backups -> one archive backup/archive-bis-<date>.zip (checked), originals -> _to_delete/
4. notes -> docs/
Every move is written to _to_delete/MANIFEST.json (original -> new) for the undo.
Usage: py cleanup/execute.py"""

import json
import os
import re
import shutil
import time
import zipfile

CLEAN = os.path.dirname(os.path.abspath(__file__))
INST = CLEAN
while not os.path.exists(os.path.join(INST, "instance.cfg")):     # the instance folder (works from cleanup/ or docs/cleanup/)
    INST = os.path.dirname(INST)
# ALREADY RUN on 2026-10-14 - running it again would move the next round of logs/backups the same way
MC = os.path.join(INST, "minecraft")
BK = os.path.join(INST, "backup")
TD = os.path.join(INST, "_to_delete")
STAMP = time.strftime("%Y-%m-%d_%H%M%S")
TODAY = time.strftime("%Y-%m-%d")


def rel(p):
    return os.path.relpath(p, INST).replace("\\", "/")


def files_of(p):
    if os.path.isfile(p):
        return [p]
    return [os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs]


def md5(p):
    import hashlib
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ the approved candidates (same rules as the plan)
cands = []
logs = os.path.join(MC, "logs")
lf = [os.path.join(logs, f) for f in os.listdir(logs)]
keep = {os.path.join(logs, "latest.log"), os.path.join(logs, "debug.log")}
for pat in (r"^\d{4}-\d\d-\d\d-\d+\.log\.gz$", r"^debug-\d+\.log\.gz$"):
    g = [f for f in lf if re.match(pat, os.path.basename(f))]
    if g:
        keep.add(max(g, key=os.path.getmtime))
cands += [f for f in lf if f not in keep and os.path.isfile(f)]                                   # S1
cr = os.path.join(MC, "crash-reports")
cands += sorted((os.path.join(cr, f) for f in os.listdir(cr)), key=os.path.getmtime)[:-1]          # S2
cands += [os.path.join(MC, "config", "DistantHorizons.toml"),                                       # S3
          os.path.join(MC, "config", "sophisticatedcore-common.toml"),                              # S4
          os.path.join(INST, "questtools", "__pycache__"),                                          # S5
          os.path.join(MC, "modernfix", "structureCacheV1"),                                        # S6
          os.path.join(MC, "essential", "cosmetic-cache")]                                          # S7
jn = os.path.join(BK, "2026-10-09_010902_jade_neat", "mods")
for f in os.listdir(jn) if os.path.isdir(jn) else []:                                              # W1
    a, b = os.path.join(jn, f), os.path.join(MC, "mods", f)
    if os.path.isfile(a) and os.path.isfile(b) and md5(a) == md5(b):
        cands.append(a)
cands.append(os.path.join(MC, "tacz_backup"))                                                      # W2
series = {}
for b in os.listdir(BK):
    m = re.match(r"^(\d{4}-\d\d-\d\d_\d{6})_(.+)$", b) or re.match(r"^(.+?)-(\d{4}-\d\d-\d\d_\d{6})$", b)
    if m:
        series.setdefault(m.group(2) if b[0].isdigit() else m.group(1), []).append(os.path.join(BK, b))
for lst in series.values():                                                                        # W3
    if len(lst) > 1:
        cands += sorted(lst, key=os.path.basename)[:-1]
cands += [os.path.join(BK, f) for f in os.listdir(BK) if f.startswith("instance.cfg.")]            # W4
cands += [os.path.join(INST, "questtools", "backups"),                                             # W5
          os.path.join(INST, "questtools", ".gamedata_cache.json"),                                # W6
          os.path.join(INST, "questtools", "validate_report.txt"),                                 # W7
          os.path.join(INST, "questtools", "balance_report.txt"),
          os.path.join(INST, "questtools", "loot_report.txt"),
          os.path.join(INST, "mod-check-report.txt"),
          os.path.join(MC, "XaeroWaypoints_BACKUP240807"),                                         # W8
          os.path.join(MC, "local", "ftbquests", "saved"),                                         # U1
          os.path.join(INST, "exports")]                                                           # U2
cands = [c for c in cands if os.path.exists(c)]
cand_norm = [os.path.normpath(c) for c in cands]


def is_cand(p):
    p = os.path.normpath(p)
    return any(p == c or p.startswith(c + os.sep) for c in cand_norm)


# old backups for the archive: everything in backup/ from before today that is not a candidate
TODAY_PREFIXES = ("bote-", "ranks-", "pfadbelohnungen-", "cleanup-", "archive-")
arch_src = []
for b in sorted(os.listdir(BK)):
    if b.startswith(TODAY_PREFIXES) or TODAY in b:
        continue
    for f in files_of(os.path.join(BK, b)):
        if not is_cand(f):
            arch_src.append(f)

DOCS = [os.path.join(INST, f) for f in ("CHANGELOG.md", "PROJECT_SUMMARY.md", "BRIEFING_FOR_CLAUDE_CHAT.md",
                                        "COMMANDS.txt", "STATUS.md")] + [os.path.join(INST, "devnotes")]
DOCS = [d for d in DOCS if os.path.exists(d)]

# ------------------------------------------------------------------ 1. safety zip
all_files = sorted({f for p in cands + arch_src + DOCS for f in files_of(p)})
safety = os.path.join(BK, f"cleanup-{STAMP}.zip")
src_bytes = sum(os.path.getsize(f) for f in all_files)
with zipfile.ZipFile(safety, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
    for f in all_files:
        z.write(f, rel(f))
with zipfile.ZipFile(safety) as z:
    bad = z.testzip()
    infos = z.infolist()
    zbytes = sum(i.file_size for i in infos)
if bad or len(infos) != len(all_files) or zbytes != src_bytes:
    raise SystemExit(f"SAFETY ZIP CHECK FAILED: bad={bad} files {len(infos)}/{len(all_files)} bytes {zbytes}/{src_bytes}")
print(f"safety zip OK: {rel(safety)}  {len(infos)} files, {src_bytes} bytes raw, {os.path.getsize(safety)} bytes zipped")

manifest = {"created": STAMP, "safety_zip": rel(safety), "moved": []}


def move(src, dst_root=TD, dst=None):
    dst = dst or os.path.join(dst_root, os.path.relpath(src, INST))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    manifest["moved"].append({"from": rel(src), "to": rel(dst)})


# ------------------------------------------------------------------ 2. candidates -> _to_delete
for c in cands:
    if os.path.exists(c):
        move(c)
print(f"moved {len(cands)} candidate paths to _to_delete/")

# ------------------------------------------------------------------ 3. archive of the old backups
arch = os.path.join(BK, f"archive-bis-{TODAY}.zip")
with zipfile.ZipFile(arch, "w", zipfile.ZIP_DEFLATED) as z:
    for f in arch_src:
        z.write(f, os.path.relpath(f, BK).replace("\\", "/"))
with zipfile.ZipFile(arch) as z:
    ok = z.testzip() is None and len(z.infolist()) == len(arch_src) and \
        sum(i.file_size for i in z.infolist()) == sum(os.path.getsize(f) for f in arch_src)
if not ok:
    raise SystemExit("ARCHIVE CHECK FAILED - nothing of the old backups was moved")
tops = sorted({os.path.relpath(f, BK).split(os.sep)[0] for f in arch_src})
for t in tops:
    move(os.path.join(BK, t))
print(f"archive OK: {rel(arch)} ({len(arch_src)} files from {len(tops)} backups); originals -> _to_delete/")

# ------------------------------------------------------------------ 4. notes -> docs/
for d in DOCS:
    move(d, dst=os.path.join(INST, "docs", os.path.basename(d)))
print("notes moved to docs/")
manifest["archive_zip"] = rel(arch)
with open(os.path.join(TD, "MANIFEST.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=1, ensure_ascii=False)
print(f"manifest: {len(manifest['moved'])} moves")
