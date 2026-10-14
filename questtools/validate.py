"""Quest validator: checks every FTB Quests file before the game starts.

Errors (exit code 1, which makes Prism cancel the launch):
  - syntax errors such as unbalanced braces or brackets, with line and column
  - duplicate or malformed IDs
  - dependencies on quests that do not exist, dependency loops, and quests blocked by those
  - item, entity, advancement, structure, dimension or stat IDs that do not exist in this instance
  - TaCZ guns, ammo or attachments that do not exist, and fire modes a gun does not have
Warnings (shown, launch continues): unescaped '&', oversized reward stacks, overlapping quests,
  overfilled magazines, quests without tasks, chapters edited in game since the last questgen run.

Usage: py validate.py [--strict] [--quiet]
  --strict   warnings also stop the launch
  --quiet    print nothing when everything is fine
"""

import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402
import snbt  # noqa: E402

QUESTS = gamedata.QUESTS_DIR
REPORT = os.path.join(HERE, "validate_report.txt")

KNOWN_TASKS = {"item", "kill", "stat", "advancement", "dimension", "structure", "checkmark", "location", "xp",
               "biome", "observation", "fluid", "gamestage", "custom", "forge_energy", "stage", "math"}
KNOWN_REWARDS = {"item", "xp", "xp_levels", "command", "loot", "random", "choice", "all_table", "toast",
                 "advancement", "custom", "stage", "gamestage", "currency"}
ID_RE = re.compile(r"^[0-9A-F]{16}$")
AMP_RE = re.compile(r"(?<!\\)&")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        self.items.append((level, where, msg))

    def error(self, where, msg):
        self.add("ERROR", where, msg)

    def warn(self, where, msg):
        self.add("WARN", where, msg)

    def info(self, where, msg):
        self.add("INFO", where, msg)

    def count(self, level):
        return sum(1 for i in self.items if i[0] == level)


class SourceFile:
    def __init__(self, path):
        self.path = path
        self.rel = os.path.relpath(path, QUESTS).replace("\\", "/")
        with open(path, encoding="utf-8") as f:
            self.text = f.read()
        self.data = None

    def line_of(self, needle, nth=0):
        idx = -1
        for _ in range(nth + 1):
            idx = self.text.find(needle, idx + 1)
            if idx < 0:
                return None
        return self.text.count("\n", 0, idx) + 1

    def where(self, needle=None, nth=0):
        ln = self.line_of(needle, nth) if needle else None
        return f"{self.rel}:{ln}" if ln else self.rel


def short(item_id):
    return item_id[10:] if item_id.startswith("minecraft:") else item_id


# --------------------------------------------------------------------------- checks

def check_item(rep, gd, src, quest_title, item, ctx, is_reward=False, count=1):
    """item is a string id or a {Count, id, tag} compound."""
    where = src.where(f'"{quest_title}"') if quest_title else src.rel
    label = f"'{quest_title}' {ctx}" if quest_title else ctx
    if isinstance(item, str):
        iid, tag = item, {}
    elif isinstance(item, dict):
        iid, tag = item.get("id", ""), item.get("tag") or {}
    else:
        rep.error(where, f"{label}: item is not a string or compound")
        return
    if not iid or iid == "minecraft:air":
        rep.error(where, f"{label}: empty item")
        return
    if ":" not in iid:
        iid = "minecraft:" + iid
    ns = iid.split(":")[0]
    if iid not in gd.items:
        if ns not in gd.namespaces:
            rep.error(where, f"{label}: item '{iid}' is from '{ns}', which is not installed")
        else:
            close = sorted(i for i in gd.items if i.startswith(ns + ":") and
                           (iid.split(":")[1] in i or i.split(":")[1] in iid))[:3]
            hint = f" (did you mean {', '.join(close)}?)" if close else ""
            rep.error(where, f"{label}: item '{iid}' does not exist{hint}")
    # TaCZ NBT
    if iid == "tacz:modern_kinetic_gun":
        gid = tag.get("GunId")
        if not gid:
            rep.error(where, f"{label}: gun without a GunId")
        elif gid not in gd.guns:
            rep.error(where, f"{label}: GunId '{gid}' is not in any installed gun pack")
        else:
            modes = gd.gun_modes(gid)
            mode = tag.get("GunFireMode")
            if mode is not None and modes and mode not in modes:
                rep.error(where, f"{label}: {gid} has no fire mode '{mode}' (valid: {', '.join(modes)})")
            elif mode is None and is_reward:
                rep.warn(where, f"{label}: {gid} has no GunFireMode; TaCZ will pick one")
            loaded = tag.get("GunCurrentAmmoCount", 0)
            mag = gd.gun_mag(gid)
            if mag and isinstance(loaded, int) and loaded > mag + 1:
                rep.warn(where, f"{label}: {gid} loaded with {loaded} rounds but the magazine holds {mag}")
    elif iid == "tacz:ammo":
        aid = tag.get("AmmoId")
        if not aid:
            rep.error(where, f"{label}: ammo without an AmmoId")
        elif aid not in gd.ammo:
            rep.error(where, f"{label}: AmmoId '{aid}' is not in any installed gun pack")
    elif iid == "tacz:attachment":
        aid = tag.get("AttachmentId")
        if not aid:
            rep.error(where, f"{label}: attachment without an AttachmentId")
        elif aid not in gd.attachments:
            rep.error(where, f"{label}: AttachmentId '{aid}' is not in any installed gun pack")
    if is_reward and count > 1:
        size = gamedata.max_stack(gd, iid, tag)
        if count > size:
            what = tag.get("AmmoId", short(iid))
            rep.warn(where, f"{label}: one reward stack of {count} {what}, but it only stacks to {size}. "
                            f"Split it (questgen does this automatically)")


def check_text(rep, src, title, field, text):
    if isinstance(text, str) and AMP_RE.search(text):
        rep.warn(src.where(text[:40]), f"'{title}' {field}: unescaped '&' (write it as \\\\& in the file; "
                                       f"questgen does this for you)")


def check_task(rep, gd, src, title, t):
    ty = t.get("type")
    where = src.where(f'"{title}"')
    if ty not in KNOWN_TASKS:
        rep.warn(where, f"'{title}': unknown task type '{ty}'")
        return
    if ty == "item":
        check_item(rep, gd, src, title, t.get("item"), "task")
    elif ty == "kill":
        e = t.get("entity", "")
        if e not in gd.entities:
            ns = e.split(":")[0]
            rep.error(where, f"'{title}': entity '{e}' " + ("is from a mod that is not installed"
                                                             if ns not in gd.namespaces else "does not exist"))
        if int(t.get("value", 1)) < 1:
            rep.error(where, f"'{title}': kill count must be at least 1")
    elif ty == "advancement":
        a = t.get("advancement", "")
        if a not in gd.advancements:
            rep.error(where, f"'{title}': advancement '{a}' does not exist")
    elif ty == "structure":
        s = t.get("structure", "")
        if s not in gd.structures:
            rep.error(where, f"'{title}': structure '{s}' does not exist")
    elif ty == "dimension":
        d = t.get("dimension", "")
        if d not in gd.dimensions:
            rep.error(where, f"'{title}': dimension '{d}' does not exist")
    elif ty == "stat":
        s = t.get("stat", "")
        if s not in gd.stats:
            rep.error(where, f"'{title}': stat '{s}' does not exist")


def check_ids(rep, files):
    seen = {}
    for src in files:
        def walk(v):
            if isinstance(v, dict):
                if "id" in v and isinstance(v["id"], str) and ("type" in v or "title" in v or "tasks" in v):
                    seen.setdefault(v["id"], []).append(src)
                    if not ID_RE.match(v["id"]):
                        rep.error(src.where(f'"{v["id"]}"'), f"ID '{v['id']}' is not 16 upper-case hex digits")
                    elif v["id"][0] in "89ABCDEF":
                        rep.error(src.where(f'"{v["id"]}"'), f"ID '{v['id']}' is too large: FTB Quests only accepts "
                                                             f"IDs up to 7FFFFFFFFFFFFFFF and will replace it in game")
                for x in v.values():
                    walk(x)
            elif isinstance(v, list):
                for x in v:
                    walk(x)
        walk(src.data)
    for qid, where in seen.items():
        if len(where) > 1:
            places = []
            counts = {}
            for s in where:
                n = counts.get(s.rel, 0)
                counts[s.rel] = n + 1
                places.append(s.where(f'id: "{qid}"', n))
            rep.error(places[0], f"ID {qid} is used {len(where)} times: {', '.join(places)}")
    return set(seen)


def check_graph(rep, quests):
    """quests: id -> (src, quest). Reports missing deps, loops and quests they block."""
    status = {}  # id -> None (ok) or reason string

    def resolve(qid, stack):
        if qid in status:
            return status[qid]
        if qid in stack:
            return "loop"
        src, q = quests[qid]
        stack.append(qid)
        reason = None
        deps = q.get("dependencies", [])
        for d in deps:
            if d not in quests:
                reason = f"depends on {d}, which does not exist"
                break
            r = resolve(d, stack)
            if r == "loop":
                reason = "is part of a dependency loop: " + " -> ".join(
                    quests[x][1].get("title", x) for x in stack[stack.index(d):] + [d])
                break
            if r:
                if q.get("dependency_requirement", "all_completed") in ("one_completed", "one_started"):
                    continue
                reason = f"can never unlock because '{quests[d][1].get('title', d)}' can't"
                break
        stack.pop()
        need = q.get("min_required_dependencies", 0)
        if not reason and need and need > len(deps):
            reason = f"needs {need} dependencies but only has {len(deps)}"
        status[qid] = reason
        return reason

    for qid in quests:
        resolve(qid, [])
    for qid, reason in status.items():
        if reason:
            src, q = quests[qid]
            rep.error(src.where(f'id: "{qid}"'), f"'{q.get('title', qid)}' is unreachable: it {reason}")


def check_generated(rep, chapter_files):
    ids_path = os.path.join(HERE, "ids.json")
    if not os.path.exists(ids_path):
        return
    try:
        with open(ids_path, encoding="utf-8") as f:
            generated = json.load(f).get("generated", {})
    except (OSError, ValueError):
        return
    for src in chapter_files:
        name = os.path.basename(src.path)[:-5]
        last = generated.get(name)
        if last and hashlib.sha256(src.text.replace("\r\n", "\n").encode("utf-8")).hexdigest() != last:
            rep.info(src.rel, "edited since the last questgen run (in game or by hand). Copy the change into "
                              "questgen.py, or the next generate will refuse to overwrite it")


def check_loot_injectors(rep, gd):
    """TaCZ loot injectors in every gun pack: valid JSON, real loot tables, real guns/ammo/attachments."""
    tacz_dir = os.path.join(gamedata.MC_DIR, "tacz")
    if not os.path.isdir(tacz_dir):
        return 0
    n = 0
    for pack in sorted(os.listdir(tacz_dir)):
        base = os.path.join(tacz_dir, pack, "data")
        if not os.path.isdir(base):
            continue
        for ns in os.listdir(base):
            d = os.path.join(base, ns, "tacz_loot_injectors")
            if not os.path.isdir(d):
                continue
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json"):
                    continue
                where = f"tacz/{pack}/{ns}/{f}"
                try:
                    with open(os.path.join(d, f), encoding="utf-8") as fh:
                        data = json.loads(gamedata.strip_json_comments(fh.read()))
                except (OSError, ValueError) as e:
                    rep.error(where, f"loot injector is not valid JSON: {e}")
                    continue
                n += 1
                tables = data.get("loot_tables") or ([data["loot_table"]] if "loot_table" in data else [])
                for t in tables:
                    if gd.loot_tables and t not in gd.loot_tables:
                        rep.warn(where, f"loot table '{t}' does not exist (mod removed?); it will just be skipped")
                if not data.get("pools"):
                    rep.error(where, "loot injector has no pools")

                def walk(entry):
                    for child in entry.get("children", []):
                        walk(child)
                    if entry.get("type") != "minecraft:item":
                        return
                    name = entry.get("name", "")
                    if name not in gd.items:
                        rep.error(where, f"loot item '{name}' does not exist")
                    for fn in entry.get("functions", []):
                        if fn.get("function") == "minecraft:set_nbt":
                            try:
                                tag = snbt.loads(fn.get("tag", "{}"))
                            except snbt.SNBTError as e:
                                rep.error(where, f"bad NBT on {name}: {e}")
                                continue
                            check_item(rep, gd, type("S", (), {"where": lambda *_: where, "rel": where})(), None,
                                       {"id": name, "tag": tag}, "loot entry")

                for pool in data.get("pools", []):
                    for e in pool.get("entries", []):
                        walk(e)
    return n


DATAPACK_DIRS = [os.path.join(gamedata.MC_DIR, "config", "paxi", "datapacks")]


def check_datapacks(rep):
    """Global (Paxi) datapacks: pack.mcmeta, JSON syntax, and that overridden mod files really exist."""
    import zipfile
    mod_files = None
    n = 0
    for base in DATAPACK_DIRS:
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            root = os.path.join(base, pack)
            if not os.path.isdir(root):
                continue
            n += 1
            try:
                import packcheck
                packcheck.check_pack(rep, root, f"datapack {pack}", check_item)
            except Exception as e:  # noqa: BLE001  never let the checker itself block a launch
                rep.warn(f"datapack {pack}", f"deep check crashed ({type(e).__name__}: {e}); basic checks still ran")
            meta = os.path.join(root, "pack.mcmeta")
            where = f"datapack {pack}"
            try:
                with open(meta, encoding="utf-8") as f:
                    fmt = json.load(f)["pack"]["pack_format"]
                if fmt != 15:
                    rep.warn(where, f"pack_format is {fmt}; Minecraft 1.20.1 uses 15")
            except (OSError, ValueError, KeyError) as e:
                rep.error(where, f"pack.mcmeta missing or invalid: {e}")
            for dirpath, _, files in os.walk(os.path.join(root, "data")):
                for fn in files:
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, root).replace("\\", "/")
                    if fn.endswith(".json"):
                        try:
                            with open(p, encoding="utf-8") as f:
                                json.load(f)
                        except ValueError as e:
                            rep.error(f"{where}: {rel}", f"invalid JSON: {e}")
                            continue
                        ns = rel.split("/")[1]
                        if ("/tags/" in rel or rel.startswith(f"data/{ns}/forge/")) and ns != "minecraft":
                            # an override of another mod's file should match a file that mod ships
                            if mod_files is None:
                                mod_files = set()
                                for kind, src in gamedata._sources():
                                    if not os.path.isdir(src):
                                        try:
                                            with zipfile.ZipFile(src) as z:
                                                mod_files.update(x for x in z.namelist() if x.startswith("data/"))
                                        except (OSError, zipfile.BadZipFile):
                                            pass
                            owner_ns_is_ours = ns.startswith("elytra") or ns == "modpack"   # our own namespaces
                            if not owner_ns_is_ours and rel not in mod_files:
                                rep.warn(f"{where}: {rel}", "overrides a file no installed mod has (typo, or the mod "
                                                            "renamed it); it does nothing")
    return n


def check_resourcepacks(rep):
    """Paxi resource packs: pack.mcmeta, and every vanilla texture override must match a real vanilla
    texture of the same size."""
    import zipfile
    import pngtool
    base = os.path.join(gamedata.MC_DIR, "config", "paxi", "resourcepacks")
    if not os.path.isdir(base):
        return
    jar = gamedata._client_jar()
    z = zipfile.ZipFile(jar) if jar else None
    try:
        for pack in sorted(os.listdir(base)):
            root = os.path.join(base, pack)
            if not os.path.isdir(root):
                continue
            where = f"resource pack {pack}"
            try:
                with open(os.path.join(root, "pack.mcmeta"), encoding="utf-8") as f:
                    fmt = json.load(f)["pack"]["pack_format"]
                if fmt != 15:
                    rep.warn(where, f"pack_format is {fmt}; Minecraft 1.20.1 resource packs use 15")
            except (OSError, ValueError, KeyError) as e:
                rep.error(where, f"pack.mcmeta missing or invalid: {e}")
            # item/block models can only use textures stitched into the block atlas (textures/block, textures/item)
            for dirpath, _, files in os.walk(os.path.join(root, "assets")):
                if os.sep + "models" not in dirpath:
                    continue
                for fn in files:
                    if not fn.endswith(".json"):
                        continue
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, root).replace("\\", "/")
                    try:
                        with open(p, encoding="utf-8") as f:
                            model = json.load(f)
                    except ValueError as e:
                        rep.error(f"{where}: {rel}", f"invalid JSON: {e}")
                        continue
                    for key, tex in (model.get("textures") or {}).items():
                        if not isinstance(tex, str) or tex.startswith("#"):
                            continue
                        ns, _, path = tex.rpartition(":")
                        ns = ns or "minecraft"
                        if not path.startswith(("block/", "item/")):
                            rep.error(f"{where}: {rel}", f"texture '{tex}' is not under block/ or item/, so it is "
                                                         f"not in the item atlas and the model renders untextured")
                            continue
                        png = os.path.join(root, "assets", ns, "textures", *path.split("/")) + ".png"
                        in_vanilla = z is not None and f"assets/{ns}/textures/{path}.png" in z.namelist()
                        if not os.path.exists(png) and not in_vanilla:
                            rep.error(f"{where}: {rel}", f"texture '{tex}' does not exist")
            for dirpath, _, files in os.walk(os.path.join(root, "assets", "minecraft", "textures")):
                for fn in files:
                    if not fn.endswith(".png") or not z:
                        continue
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, root).replace("\\", "/")
                    with open(p, "rb") as f:
                        data = f.read()
                    try:
                        mine = pngtool.size(data)
                    except Exception:  # noqa: BLE001
                        rep.error(f"{where}: {rel}", "not a valid PNG")
                        continue
                    try:
                        vanilla = pngtool.size(z.read(rel))
                    except KeyError:
                        rep.warn(f"{where}: {rel}", "replaces no vanilla texture (wrong path?); it does nothing")
                        continue
                    if mine != vanilla:
                        rep.warn(f"{where}: {rel}", f"is {mine[0]}x{mine[1]} but the vanilla texture is "
                                                    f"{vanilla[0]}x{vanilla[1]}; the model may look broken")
    finally:
        if z:
            z.close()


def validate():
    rep = Report()
    gd = gamedata.load()
    if not gd.has_client:
        rep.warn("(setup)", "Minecraft client jar not found; vanilla IDs can't be checked properly")

    files = []
    for root, _, names in os.walk(QUESTS):
        for n in sorted(names):
            if n.endswith(".snbt"):
                files.append(SourceFile(os.path.join(root, n)))
    good = []
    for src in files:
        try:
            src.data = snbt.loads(src.text)
            good.append(src)
        except snbt.SNBTError as e:
            rep.error(f"{src.rel}:{e.line}", f"syntax error, col {e.col}: {e.msg}")

    check_ids(rep, good)

    groups = {}
    gsrc = next((s for s in good if s.rel == "chapter_groups.snbt"), None)
    if gsrc:
        groups = {g.get("id"): g.get("title") for g in gsrc.data.get("chapter_groups", [])}

    chapter_files = [s for s in good if s.rel.startswith("chapters/")]
    quests = {}
    orders = {}
    titles = {}
    for src in chapter_files:
        c = src.data
        if not isinstance(c, dict) or "quests" not in c:
            rep.error(src.rel, "not a chapter file (no quests list)")
            continue
        stem = os.path.basename(src.path)[:-5]
        if c.get("filename") != stem:
            rep.error(src.where("filename:"), f"filename is '{c.get('filename')}' but the file is {stem}.snbt")
        if groups and c.get("group") and c["group"] not in groups:
            rep.error(src.where("group:"), f"chapter group {c['group']} does not exist in chapter_groups.snbt")
        key = (c.get("group"), c.get("order_index"))
        if key in orders:
            rep.warn(src.where("order_index"), f"same order_index {key[1]} as {orders[key]} in this group")
        orders[key] = stem
        t = c.get("title", stem)
        if t in titles:
            rep.warn(src.where("title:"), f"chapter title '{t}' is also used by {titles[t]}")
        titles[t] = stem
        if "icon" in c:
            check_item(rep, gd, src, None, c["icon"], "chapter icon")
        spots = {}
        for q in c["quests"]:
            title = q.get("title", q.get("id", "?"))
            quests[q.get("id")] = (src, q)
            for field in ("title", "subtitle"):
                check_text(rep, src, title, field, q.get(field))
            for line in q.get("description", []):
                check_text(rep, src, title, "description", line)
            if not q.get("tasks"):
                rep.warn(src.where(f'"{title}"'), f"'{title}' has no tasks")
            for t in q.get("tasks", []):
                check_task(rep, gd, src, title, t)
            for r in q.get("rewards", []):
                ty = r.get("type")
                if ty not in KNOWN_REWARDS:
                    rep.warn(src.where(f'"{title}"'), f"'{title}': unknown reward type '{ty}'")
                if ty == "item":
                    check_item(rep, gd, src, title, r.get("item"), "reward", True, int(r.get("count", 1)))
            if "icon" in q:
                check_item(rep, gd, src, title, q["icon"], "icon")
            pos = (float(q.get("x", 0)), float(q.get("y", 0)))
            if pos in spots:
                rep.warn(src.where(f'"{title}"'), f"'{title}' sits on top of '{spots[pos]}' at {pos}")
            spots[pos] = title
    check_graph(rep, quests)
    check_generated(rep, chapter_files)
    check_loot_injectors(rep, gd)
    check_datapacks(rep)
    check_resourcepacks(rep)
    return rep, len(chapter_files), len(quests)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    strict, quiet = "--strict" in argv, "--quiet" in argv
    rep, nch, nq = validate()
    # elytra_hordes uses two code-registered entities (no lang keys, so packcheck can't see them);
    # hordecheck.py verifies those in the jar classes plus the pack's settings/objectives.
    if os.path.isdir(os.path.join(gamedata.MC_DIR, "config", "paxi", "datapacks", "elytra_hordes")):
        import contextlib
        import io
        try:
            import hordecheck
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = hordecheck.main()
            if rc:
                for line in buf.getvalue().splitlines():
                    if line.startswith("ERROR"):
                        rep.error("datapack elytra_hordes", line[5:].strip())
        except Exception as e:  # noqa: BLE001
            rep.warn("datapack elytra_hordes", f"hordecheck crashed ({type(e).__name__}: {e})")
    errs, warns = rep.count("ERROR"), rep.count("WARN")
    out = []
    for level in ("ERROR", "WARN", "INFO"):
        rows = [i for i in rep.items if i[0] == level]
        if rows:
            out.append(f"{level} ({len(rows)})")
            out.extend(f"  {w}  {m}" for _, w, m in rows)
            out.append("")
    verdict = "FAILED" if errs or (strict and warns) else "OK"
    out.append(f"Quest check {verdict}: {nch} chapters, {nq} quests, {errs} error(s), {warns} warning(s).")
    text = "\n".join(out)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    if not quiet or verdict != "OK" or warns:
        print(text)
    return 1 if verdict == "FAILED" else 0


if __name__ == "__main__":
    sys.exit(main())
