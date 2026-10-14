"""Independent re-count for the quest audit: plain text/regex over the .snbt files (no SNBT parser),
compared with the numbers in audit/quests.csv. Read only. Usage: py audit/verify_counts.py"""

import csv
import os
import re
import sys

AUDIT = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(os.path.dirname(AUDIT), "minecraft", "config", "ftbquests", "quests", "chapters")

text_q = text_rep = 0
text_rt = {"gun": 0, "ammo": 0, "att": 0, "rocket": 0, "shulker": 0}
per_file = {}
for f in sorted(os.listdir(CH)):
    s = open(os.path.join(CH, f), encoding="utf-8").read()
    # a quest = an object that has an x: coordinate line ("x: 1.0d") at quest indentation (2 tabs)
    # (single-element lists are written inline as "[{", so quests sit at 2 or 3 tabs)
    nq = len(re.findall(r"^\t{2,3}x: ", s, re.M))
    rep = len(re.findall(r"^\t{2,3}can_repeat: true", s, re.M))
    per_file[f] = nq
    text_q += nq
    text_rep += rep
    rewards = []
    for m in re.finditer(r"rewards: \[", s):       # cut out each rewards list by bracket matching
        depth, i = 0, m.end() - 1
        while True:
            depth += {"[": 1, "]": -1}.get(s[i], 0)
            if depth == 0:
                break
            i += 1
        rewards.append(s[m.end():i])
    for block in rewards:
        def n(iid):
            return len(re.findall(r'(?:id|item): "%s"' % iid, block))
        text_rt["gun"] += n("tacz:modern_kinetic_gun")
        text_rt["ammo"] += n("tacz:ammo")
        text_rt["att"] += n("tacz:attachment")
        text_rt["rocket"] += n("minecraft:firework_rocket")
        text_rt["shulker"] += n(r"minecraft:\w*shulker_box")

rows = list(csv.DictReader(open(os.path.join(AUDIT, "quests.csv"), encoding="utf-8-sig"), delimiter=";"))
csv_rep = sum(1 for r in rows if r["wiederholbar"] == "ja")
csv_shop = sum(1 for r in rows if r["Kategorie"] == "Shop")
csv_per_file = {}
for r in rows:
    csv_per_file[r["Kapitel-Datei"]] = csv_per_file.get(r["Kapitel-Datei"], 0) + 1

ok = True
def check(name, a, b):
    global ok
    good = a == b
    ok &= good
    print(f"{'OK ' if good else 'DIFF'} {name}: text={a} csv/report={b}")

check("quests", text_q, len(rows))
check("wiederholbar", text_rep, csv_rep)
check("shop (all repeatable quests are shop entries)", text_rep, csv_shop)
for f in per_file:
    if per_file[f] != csv_per_file.get(f):
        check(f"quests in {f}", per_file[f], csv_per_file.get(f))
print("reward entries by text:", text_rt)
report = open(os.path.join(AUDIT, "QUEST_AUDIT.md"), encoding="utf-8").read()
m = re.search(r"\*\*Summe\*\* \| 26 Kapitel \|  \|  \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+)", report)
if m:
    for name, idx in (("gun", 3), ("ammo", 4), ("att", 5), ("rocket", 6), ("shulker", 7)):
        check(f"reward entries {name}", text_rt[name], int(m.group(idx)))
else:
    ok = False
    print("DIFF: sum row not found in report")
sys.exit(0 if ok else 1)
