"""
Interactive quest maker:  py questadd.py   (or double-click questadd.cmd)

Asks step by step for chapter, title, task, reward, text, predecessor and position, checks every
ID against the installed mods, shows the finished quest, adds it to questgen.py and regenerates the
chapter (the validator runs too). If anything fails, questgen.py is restored automatically.
"""

import datetime
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
import questlib  # noqa: E402

QG = os.path.join(HERE, "questgen.py")

TASK_HELP = """  Task examples:
    adv story/smelt_iron          vanilla advancement (adv <namespace:>path)
    have copper_ingot             have 1 copper ingot (kept)      have 16 iron_ingot
    give 6 gold_ingot             hand in 6 gold (taken away)
    kill zombie 10                kill aether:slider 1
    dim the_nether                structure ancient_city          fly 25km      playtime 10h
    check                         a box the player ticks
  Several tasks: separate with ;   e.g.  have copper_ingot; have iron_ingot"""
REWARD_HELP = """  Reward examples:
    aether:golden_oak_sapling     16 ammo:9mm       gun:glock_17      att:sight_t1
    6 gold_ingot, 3 diamond       (several rewards: separate with commas)"""


def ask(prompt, default=None):
    tip = f" [{default}]" if default not in (None, "") else ""
    try:
        v = input(f"{prompt}{tip}: ").replace("﻿", "").strip()
    except EOFError:
        sys.exit(0)
    return v if v else (default or "")


def chapters(src):
    out = []
    for m in re.finditer(r"^    Chapter\('([^']+)', (['\"])(.*?)\2", src, re.M):
        start = m.start()
        end = src.index("\n    ]),\n", start) + 1
        block = src[start:end]
        quests = []
        for qm in re.finditer(r"\n        Q\((['\"])(.*?)\1,", block):
            nxt = block.find("\n        Q(", qm.end())
            body = block[qm.start(): nxt if nxt > 0 else len(block)]
            at = re.search(r"at=\(([-\d.]+), ([-\d.]+)\)", body)
            quests.append((qm.group(2), (float(at.group(1)), float(at.group(2))) if at else None))
        out.append({"file": m.group(1), "title": m.group(3), "end": end, "quests": quests})
    return out


def check_ids(tasks, rewards):
    gd = gamedata.load()
    bad = []
    for t in tasks:
        kw = t.kw
        if t.kind == "item":
            bad += check_item(gd, kw["item"])
        elif t.kind == "kill" and kw["entity"] not in gd.entities:
            bad.append(f"entity '{kw['entity']}'")
        elif t.kind == "advancement" and kw["adv"] not in gd.advancements:
            bad.append(f"advancement '{kw['adv']}'")
        elif t.kind == "dimension" and kw["dim"] not in gd.dimensions:
            bad.append(f"dimension '{kw['dim']}'")
        elif t.kind == "structure" and kw["structure"].lstrip("#") not in gd.structures:
            bad.append(f"structure '{kw['structure']}'")
        elif t.kind == "stat" and kw["stat"] not in gd.stats:
            bad.append(f"stat '{kw['stat']}'")
    for r in rewards:
        bad += check_item(gd, r)
    return bad


def check_item(gd, it):
    if it.kind == "gun":
        return [] if it.ref in gd.guns else [f"gun '{it.ref}'"]
    if it.kind == "ammo":
        return [] if it.ref in gd.ammo else [f"ammo '{it.ref}'"]
    if it.kind == "attachment":
        return [] if it.ref in gd.attachments else [f"attachment '{it.ref}'"]
    return [] if it.id in gd.items else [f"item '{it.id}'"]


def ask_parsed(prompt, helptext, parse, kind):
    print(helptext)
    while True:
        spec = ask(prompt)
        if not spec:
            print("  (required)")
            continue
        try:
            parsed = parse(spec)
        except Exception as e:  # noqa: BLE001
            print(f"  Not understood: {e}")
            continue
        bad = check_ids(parsed, []) if kind == "task" else check_ids([], parsed)
        if bad:
            print("  Does not exist in this pack: " + ", ".join(bad) + ". Try again.")
            continue
        return spec


def one_quest():
    src = open(QG, encoding="utf-8").read()
    chs = chapters(src)
    print("\nChapters:")
    for n, c in enumerate(chs, 1):
        print(f"  {n:2}. {c['title']}  ({c['file']}, {len(c['quests'])} quests)")
    while True:
        v = ask("Chapter number")
        if v.isdigit() and 1 <= int(v) <= len(chs):
            ch = chs[int(v) - 1]
            break
    titles = [q[0] for q in ch["quests"]]
    while True:
        title = ask("Quest title")
        if title and title not in titles:
            break
        print("  Needs a title that is not used in this chapter yet.")
    task = ask_parsed("Task", TASK_HELP, questlib.parse_task, "task")
    reward = ask_parsed("Reward", REWARD_HELP, questlib.parse_items, "reward")
    print("Description: type the text; each Enter starts a new line, an empty line finishes.")
    desc = []
    while True:
        line = input("  > ").replace("﻿", "").rstrip()
        if not line:
            break
        desc.append(line)
    after = []
    if ch["quests"]:
        print("Predecessor (the quest that must be done first; with hiding on, this quest stays invisible until then):")
        for n, (t, at) in enumerate(ch["quests"], 1):
            print(f"  {n:2}. {t}  at {at}")
        v = ask("Number(s), comma-separated, or Enter for none")
        for part in v.replace(" ", "").split(","):
            if part.isdigit() and 1 <= int(part) <= len(ch["quests"]):
                after.append(ch["quests"][int(part) - 1][0])
    pos = dict(ch["quests"])
    if after and pos.get(after[0]):
        px, py_ = pos[after[0]]
        default = (px + 1.5, py_)
    else:
        top = [at[0] for _, at in ch["quests"] if at and at[1] == 0]
        default = (max(top) + 1.5, 0.0) if top else (0.0, 0.0)
    print("Position: Enter = default (right of the predecessor, or next free spot in the top row),")
    print("          'b' = below the predecessor, or two numbers 'x y' (1.5 apart = neighbours).")
    while True:
        v = ask("Position", f"{default[0]:g} {default[1]:g}")
        if v.lower() == "b" and after and pos.get(after[0]):
            at = (pos[after[0]][0], pos[after[0]][1] + 1.5)
            break
        try:
            x, y = (float(p) for p in v.replace(",", " ").split())
            at = (x, y)
            break
        except ValueError:
            print("  Use 'x y', e.g. 1.5 0")
    icon = ask("Icon item (Enter = automatic)")
    if icon:
        try:
            if check_item(gamedata.load(), questlib.parse_item(icon)):
                print("  Unknown icon item, using automatic.")
                icon = ""
        except Exception:  # noqa: BLE001
            icon = ""

    def lit(v):
        return repr(v)
    kws = []
    if desc:
        kws.append("desc=" + (lit(desc[0]) if len(desc) == 1 else lit(desc)))
    kws.append(f"at=({at[0]:g}, {at[1]:g})")
    if after:
        kws.append("after=" + (lit(after[0]) if len(after) == 1 else lit(after)))
    if icon:
        kws.append(f"icon={lit(icon)}")
    line = (f"        Q({lit(title)}, {lit(task)}, {lit(reward)},\n"
            f"          {', '.join(kws)}),\n")
    print("\nNew quest:\n" + line)
    if ask("Add it? (y/n)", "y").lower() not in ("y", "j", "yes", "ja"):
        print("Not added.")
        return
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    bdir = os.path.join(HERE, "backups")
    os.makedirs(bdir, exist_ok=True)
    backup = os.path.join(bdir, f"questgen_before_questadd_{stamp}.py")
    shutil.copy2(QG, backup)
    insert_at = ch["end"]   # start of the chapter's closing "    ])," line
    new_src = src[:insert_at] + line + src[insert_at:]
    with open(QG, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_src)
    r = subprocess.run([sys.executable, QG, "--only", ch["file"]], cwd=HERE)
    if r.returncode != 0:
        shutil.copy2(backup, QG)
        print("\nSomething failed (see above). questgen.py was restored; nothing changed.")
    else:
        print(f"\nDone. In game: /ftbquests reload   (questgen.py backup: backups/{os.path.basename(backup)})")


def main():
    print("Quest maker for the Elysius quest book. Ctrl+C quits at any time.")
    try:
        while True:
            one_quest()
            if ask("\nAnother quest? (y/n)", "n").lower() not in ("y", "j", "yes", "ja"):
                break
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()
