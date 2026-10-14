"""Extra checks for the elytra_hordes Paxi datapack (zombie hordes + TaCZ gunfire noise).

Run:  python questtools/hordecheck.py      (exit code 0 = OK, 1 = errors)

Covers what packcheck.py cannot see:
- entity IDs registered in mod code without a lang key (gamedata only knows lang-key entities):
  zombieawareness:scent and tacz:bullet are looked up in the jars' class files, and every id the pack
  uses in entity tags or single-quoted passenger NBT must be known to gamedata or verified that way
- the Zombie Awareness scent NBT keys the pack writes (age, strengthpeak, type) exist in EntityScent
- every #setting mh_cfg / #const mh_const the functions read is set in settings.mcfunction / load.mcfunction
- every mh_* objective used is created in load.mcfunction
- JSON files parse
"""

import json
import os
import re
import sys
import zipfile

import gamedata

PACK = os.path.join(gamedata.MC_DIR, "config", "paxi", "datapacks", "elytra_hordes")
MODS = os.path.join(gamedata.MC_DIR, "mods")

# id -> (jar name prefix, class file, byte strings that must all be in it)
CODE_ENTITIES = {
    "zombieawareness:scent": ("zombieawareness", "com/corosus/zombieawareness/EntityRegistry.class",
                              [b"zombieawareness", b"scent"]),
    "tacz:bullet": ("tacz", "com/tacz/guns/init/ModEntities.class", [b"tacz", b"bullet"]),
}
SCENT_CLASS = ("zombieawareness", "com/corosus/zombieawareness/EntityScent.class",
               [b"age", b"strengthpeak", b"type"])


def _jar_has(prefix, cls, needles):
    for f in os.listdir(MODS):
        if f.lower().startswith(prefix) and f.endswith(".jar"):
            with zipfile.ZipFile(os.path.join(MODS, f)) as z:
                try:
                    data = z.read(cls)
                except KeyError:
                    return False, f"{f} has no {cls}"
            missing = [n.decode() for n in needles if n not in data]
            return (not missing), (f"{f}: {cls} lacks {missing}" if missing else f)
    return False, f"no {prefix}*.jar in mods/"


def main():
    errors, notes = [], []
    gd = gamedata.load()
    verified = set()
    for eid, (prefix, cls, needles) in CODE_ENTITIES.items():
        ok, msg = _jar_has(prefix, cls, needles)
        (verified.add(eid) if ok else errors.append(f"{eid}: {msg}"))
        if ok:
            notes.append(f"{eid}: registered in {msg}")
    ok, msg = _jar_has(*SCENT_CLASS)
    if not ok:
        errors.append(f"scent NBT keys: {msg}")

    known = gd.entities | verified
    funcs = {}
    for dirpath, _, files in os.walk(os.path.join(PACK, "data")):
        for fn in files:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, PACK).replace("\\", "/")
            if fn.endswith(".json"):
                try:
                    with open(p, encoding="utf-8") as fh:
                        d = json.load(fh)
                except ValueError as e:
                    errors.append(f"{rel}: invalid JSON: {e}")
                    continue
                if "/tags/entity_types/" in rel:
                    for v in d.get("values", []):
                        v = v.get("id") if isinstance(v, dict) else v
                        if not v.startswith("#") and v not in known:
                            errors.append(f"{rel}: entity '{v}' not found")
            elif fn.endswith(".mcfunction"):
                with open(p, encoding="utf-8") as fh:
                    funcs[rel] = fh.read()

    settings = "".join(t for r, t in funcs.items() if r.endswith(("horde/settings.mcfunction", "horde/load.mcfunction")))
    defined_cfg = set(re.findall(r"scoreboard players (?:set|operation) (#[\w-]+) mh_cfg", settings))
    defined_const = set(re.findall(r"scoreboard players set (#[\w-]+) mh_const", settings))
    created = set(re.findall(r"scoreboard objectives add (mh_\w+)", settings))
    for rel, text in funcs.items():
        for n, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            for eid in re.findall(r"\bid:'([a-z0-9_.-]+:[a-z0-9_/.-]+)'", line):
                if eid not in known:
                    errors.append(f"{rel}:{n}: entity '{eid}' not found")
            for name in re.findall(r"(#[\w-]+) mh_cfg", line):
                if name not in defined_cfg:
                    errors.append(f"{rel}:{n}: setting {name} mh_cfg is never set")
            for name in re.findall(r"(#[\w-]+) mh_const", line):
                if name not in defined_const:
                    errors.append(f"{rel}:{n}: constant {name} mh_const is never set")
            for obj in re.findall(r"\b(mh_[a-z_]+)\b", line):
                if obj not in created and not obj.startswith(("mh_spawn", "mh_rng", "mh_probe", "mh_spot",
                                                             "mh_new", "mh_force", "mh_heard", "mh_sense",
                                                             "mh_gun_sense", "mh_lure_sense", "mh_init",
                                                             "mh_carrier")):
                    errors.append(f"{rel}:{n}: objective/tag '{obj}' is not created in load.mcfunction")
    for x in notes:
        print("ok  ", x)
    for x in errors:
        print("ERROR", x)
    print(f"hordecheck: {len(funcs)} functions, {len(defined_cfg)} settings, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
