"""Engine behind questgen.py: turns the data table into FTB Quests chapter files.

You normally only edit questgen.py. This file handles the parts that should never be done by hand:
stable unique IDs (ids.json), '&' escaping, splitting big rewards into legal stack sizes,
generated price / reward text, layout, backups and the in-game-edit safety check.
"""

import argparse
import datetime
import difflib
import hashlib
import json
import os
import random
import re
import shutil
import sys

import gamedata
import snbt
from snbt import Byte, Double, Long

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(gamedata.QUESTS_DIR, "chapters")
GROUPS_FILE = os.path.join(gamedata.QUESTS_DIR, "chapter_groups.snbt")
IDS_FILE = os.path.join(HERE, "ids.json")
BACKUP_DIR = os.path.join(HERE, "backups")

ALIASES = {"rocket": "minecraft:firework_rocket", "rockets": "minecraft:firework_rocket"}


class QuestError(Exception):
    pass


# =========================================================== text helpers

def esc(text):
    """FTB Quests treats '&' as a colour code. Escape every '&' so it shows literally.
    Use the section sign (e.g. '§a') if you really want colours."""
    if text is None:
        return None
    return re.sub(r"(?<!\\)&", r"\\&", text)


def lines(x):
    if x is None:
        return []
    return [x] if isinstance(x, str) else list(x)


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


# =========================================================== item specs

class Item:
    """One item stack: id + optional NBT tag + count."""

    def __init__(self, item_id, count=1, tag=None, kind=None, ref=None):
        self.id, self.count, self.tag = item_id, count, tag
        self.kind, self.ref = kind, ref  # kind: gun / ammo / attachment / None, ref: the TaCZ id

    def with_count(self, n):
        return Item(self.id, n, self.tag, self.kind, self.ref)

    def same_stack(self, other):
        return self.id == other.id and self.tag == other.tag

    def nbt(self):
        if not self.tag:
            return self.id
        return {"Count": 1, "id": self.id, "tag": self.tag}

    def icon_nbt(self):
        # quest icons only need enough NBT to pick the right model
        if self.kind == "gun":
            return {"Count": 1, "id": self.id, "tag": {"GunId": self.ref}}
        return self.nbt()


def _ns(rid, default="minecraft"):
    return rid if ":" in rid else f"{default}:{rid}"


def _split_top(text, seps):
    """Split on any separator in seps, ignoring separators inside {...} or quotes."""
    out, depth, cur, i, q = [], 0, [], 0, None
    while i < len(text):
        c = text[i]
        if q:
            cur.append(c)
            if c == "\\":
                cur.append(text[i + 1:i + 2])
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
            cur.append(c)
        elif c in "{[":
            depth += 1
            cur.append(c)
        elif c in "}]":
            depth -= 1
            cur.append(c)
        elif depth == 0 and any(text.startswith(s, i) for s in seps):
            sep = next(s for s in seps if text.startswith(s, i))
            out.append("".join(cur))
            cur = []
            i += len(sep)
            continue
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur))
    return [x.strip() for x in out if x.strip()]


def parse_item(spec):
    """'6 gold_ingot', 'gun:glock_17', 'gun:db_short@BURST', 'gun:m1911 loaded', '60 ammo:9mm',
    'att:sight_552', 'aether:zanite_gemstone', 'elytra{Damage:0,Unbreakable:1b}'."""
    if isinstance(spec, Item):
        return spec
    if isinstance(spec, _Special):
        return spec.item()
    s = spec.strip()
    count = 1
    m = re.match(r"^(\d+)\s*x?\s+(.*)$", s)
    if m:
        count, s = int(m.group(1)), m.group(2).strip()
    loaded = False
    if s.endswith(" loaded"):
        loaded, s = True, s[:-7].strip()
    tag = None
    if "{" in s:
        s, raw = s[:s.index("{")], s[s.index("{"):]
        tag = snbt.loads(raw)
    s = s.strip()
    if s.startswith("gun:"):
        body = s[4:]
        mode = None
        if "@" in body:
            body, mode = body.split("@", 1)
        gid = _ns(body, "tacz")
        modes = gamedata.load().gun_modes(gid)
        mode = (mode or (modes[0] if modes else "SEMI")).upper()
        t = {"GunCurrentAmmoCount": 0, "GunFireMode": mode, "GunId": gid}
        if loaded:
            t["GunCurrentAmmoCount"] = gamedata.load().gun_mag(gid) or 0
            t["HasBulletInBarrel"] = Byte(1)
        if tag:
            t.update(tag)
        return Item("tacz:modern_kinetic_gun", count, t, "gun", gid)
    if s.startswith("ammo:"):
        aid = _ns(s[5:], "tacz")
        return Item("tacz:ammo", count, {"AmmoId": aid}, "ammo", aid)
    if s.startswith(("att:", "attachment:")):
        aid = _ns(s.split(":", 1)[1], "tacz")
        return Item("tacz:attachment", count, {"AttachmentId": aid}, "attachment", aid)
    rid = ALIASES.get(s, _ns(s))
    return Item(rid, count, tag)


class command:
    """FTB command reward: command("/execute as @p at @s run function ns:fn"). auto="invisible" runs it on
    completion without showing it in the quest window (no spoilers)."""

    def __init__(self, cmd, auto="invisible", elevate=True, silent=True):
        self.cmd, self.auto, self.elevate, self.silent = cmd, auto, elevate, silent

    def nbt(self):
        return {"auto": self.auto, "command": self.cmd, "elevate_perms": self.elevate, "silent": self.silent,
                "type": "command"}


def parse_items(spec):
    if spec is None:
        return []
    if isinstance(spec, command):
        return [spec]
    if isinstance(spec, (list, tuple)):
        out = []
        for x in spec:
            out.extend(parse_items(x))
        return out
    if isinstance(spec, (Item, _Special)):
        return [parse_item(spec)]
    return [parse_item(p) for p in _split_top(spec, [",", " + "])]


class _Special:
    def item(self):
        raise NotImplementedError


class book(_Special):
    """A written book from the BOOKS table: book("dark_sun")."""
    registry = {}

    def __init__(self, key):
        self.key = key

    def item(self):
        b = book.registry.get(self.key)
        if not b:
            raise QuestError(f"book '{self.key}' is not in BOOKS")
        pages = [p if p.lstrip().startswith("{") else json.dumps({"text": p}, ensure_ascii=False)
                 for p in b["pages"]]
        tag = {"author": b.get("author", ""), "pages": pages, "resolved": Byte(1), "title": b["title"]}
        return Item("minecraft:written_book", 1, tag)


class named(_Special):
    """An item with a custom (non-italic) name: named("red_shulker_box", "Hero's Box")."""

    def __init__(self, item_id, name, count=1):
        self.item_id, self.name, self.count = item_id, name, count

    def item(self):
        base = parse_item(self.item_id)
        tag = dict(base.tag or {})
        tag["display"] = {"Name": json.dumps({"text": self.name, "italic": False}, ensure_ascii=False)}
        return Item(base.id, self.count, tag)


# =========================================================== tasks

class Task:
    def __init__(self, kind, **kw):
        self.kind, self.kw = kind, kw

    def nbt(self, tid):
        k, kw = self.kind, self.kw
        if k == "item":
            d = {"id": tid, "item": kw["item"].nbt(), "type": "item"}
            if kw["consume"]:
                d["consume_items"] = True
            if kw["item"].count != 1:
                d["count"] = Long(kw["item"].count)
            return d
        if k == "kill":
            return {"entity": kw["entity"], "id": tid, "type": "kill", "value": Long(kw["value"])}
        if k == "stat":
            return {"id": tid, "stat": kw["stat"], "type": "stat", "value": int(kw["value"])}
        if k == "advancement":
            return {"advancement": kw["adv"], "criterion": kw.get("criterion", ""), "id": tid, "type": "advancement"}
        if k == "dimension":
            return {"dimension": kw["dim"], "id": tid, "type": "dimension"}
        if k == "structure":
            return {"id": tid, "structure": kw["structure"], "type": "structure"}
        if k == "checkmark":
            return {"id": tid, "type": "checkmark"}
        if k == "raw":
            d = dict(kw["data"])
            d["id"] = tid
            return d
        raise QuestError(f"unknown task kind {k}")


def parse_task(spec):
    """'give 6 gold_ingot' (consumed), 'have 6 gold_ingot' (kept), 'kill zombie 10', 'fly 25km',
    'playtime 10h', 'stat mob_kills 250', 'adv story/smelt_iron', 'dim the_nether',
    'structure pillager_outpost', 'check'. Several tasks: a list, or separated by ';'."""
    if isinstance(spec, Task):
        return [spec]
    if isinstance(spec, (list, tuple)):
        out = []
        for x in spec:
            out.extend(parse_task(x))
        return out
    if ";" in spec:
        return parse_task([p for p in spec.split(";") if p.strip()])
    s = spec.strip()
    word, _, rest = s.partition(" ")
    rest = rest.strip()
    w = word.lower()
    if w in ("give", "have"):
        return [Task("item", item=it, consume=(w == "give")) for it in parse_items(rest)]
    if w == "kill":
        m = re.match(r"^(\S+)(?:\s+(\d+))?$", rest)
        if not m:
            raise QuestError(f"bad kill task '{spec}' (use: kill zombie 10)")
        return [Task("kill", entity=_ns(m.group(1)), value=int(m.group(2) or 1))]
    if w == "fly":
        m = re.match(r"^([\d.]+)\s*km$", rest)
        if not m:
            raise QuestError(f"bad fly task '{spec}' (use: fly 25km)")
        return [Task("stat", stat="minecraft:aviate_one_cm", value=round(float(m.group(1)) * 100000))]
    if w == "playtime":
        m = re.match(r"^([\d.]+)\s*h$", rest)
        if not m:
            raise QuestError(f"bad playtime task '{spec}' (use: playtime 10h)")
        return [Task("stat", stat="minecraft:play_time", value=round(float(m.group(1)) * 72000))]
    if w == "stat":
        m = re.match(r"^(\S+)\s+(\d+)$", rest)
        if not m:
            raise QuestError(f"bad stat task '{spec}' (use: stat mob_kills 250)")
        return [Task("stat", stat=_ns(m.group(1)), value=int(m.group(2)))]
    if w in ("adv", "advancement"):
        adv, _, crit = rest.partition(" ")
        return [Task("advancement", adv=_ns(adv), criterion=crit.strip())]
    if w in ("dim", "dimension"):
        return [Task("dimension", dim=_ns(rest))]
    if w == "structure":
        return [Task("structure", structure=rest if rest.startswith("#") else _ns(rest))]
    if w in ("check", "checkmark"):
        return [Task("checkmark")]
    raise QuestError(f"unknown task '{spec}'")


# =========================================================== quests

class Q:
    """One quest row: Q(title, task, reward, desc=..., sub=..., at=(x, y), after=[...], icon=..., ...)."""

    def __init__(self, title, task, reward, desc=None, sub=None, at=None, after=None, icon=None,
                 repeat=None, optional=False, key=None, auto=None, extra=None):
        self.title = title
        self.tasks = parse_task(task)
        self.rewards = parse_items(reward)
        self.desc = desc
        self.sub = sub
        self.at = at
        self.after = [after] if isinstance(after, (str, tuple)) else list(after or [])
        self.icon = icon
        self.repeat = repeat
        self.optional = optional
        self.key = key or title
        self.auto = auto
        self.extra = extra or {}
        self.section = None      # layout: a new section starts a new row block
        self.pair = None         # layout: 0 = top of a single/bulk pair, 1 = bottom
        self.auto_desc = None    # callable(ctx) -> list of lines, used when desc is None
        self.auto_sub = None


def gun(gun_id, name, price, tier, mode=None, note=None):
    """Gun shop row. gun("glock_17", "Glock 17", "10 gold_ingot", "Gold tier")."""
    spec = f"gun:{gun_id}" + (f"@{mode}" if mode else "")
    q = Q(name, ["give " + p for p in _split_top(price, [",", " + "])], spec, sub=tier,
          icon=f"gun:{gun_id}")
    q.section = tier
    q.gun_name = (_ns(gun_id, "tacz"), name)
    q.auto_desc = lambda ctx: [f"Price: {ctx.price_text(q)}.",
                               note or "Ammo: see the Ammo chapters. Attachments: see the Attachments chapters."]
    return q


def ammo(ammo_id, name, price, per=1, bulk=None, fits=None):
    """Ammo trade pair: ammo("9mm", "9mm", "1 copper_ingot", per=5) = 1 copper for 5 rounds,
    plus a bulk trade for one full stack of that calibre (12 copper for 60 rounds)."""
    aid = _ns(ammo_id, "tacz")
    if bulk is None:
        stack = gamedata.load().ammo_stack(aid)
        if stack % per:
            raise QuestError(f"ammo {ammo_id}: a stack is {stack} rounds, which is not a multiple of per={per}. "
                             f"Pick a per that divides {stack}")
        bulk = stack // per
    out = []
    for i, mult in enumerate((1, bulk)):
        cost = [p.with_count(p.count * mult) for p in parse_items(price)]
        n = per * mult
        q = Q(f"{name} Ammo" + (f" x{n}" if i else ""), [Task("item", item=c, consume=True) for c in cost],
              f"{n} ammo:{ammo_id}", icon=f"ammo:{ammo_id}")
        q.pair = i
        q.ammo_name = (aid, name)

        def d(ctx, q=q, n=n, cost=cost):
            guns = fits if fits is not None else ctx.guns_using(aid)
            return [f"{ctx.items_text(cost)} = {plural(n, 'round')} of {name}.",
                    "Fits: " + (", ".join(guns) if guns else "no gun in the installed gun packs (other packs may use it)")]

        def s(ctx):
            guns = fits if fits is not None else ctx.guns_using(aid)
            if not guns:
                return "No gun uses this yet"
            return "Uses: " + ", ".join(guns[:3]) + (f" +{len(guns) - 3}" if len(guns) > 3 else "")

        q.auto_desc, q.auto_sub = d, s
        out.append(q)
    return out


def att(att_id, name, price):
    """Attachment shop row. att("sight_552", "552 Sight", "12 iron_ingot + 5 gold_ingot")."""
    q = Q(name, ["give " + p for p in _split_top(price, [",", " + "])], f"att:{att_id}", icon=f"att:{att_id}")
    q.auto_desc = lambda ctx: [f"Price: {ctx.price_text(q)}.", ctx.chapter.note or ""]
    return q


def rockets(source, per, bulk=16):
    """Rocket trade pair. rockets("gunpowder", 8) = 1 gunpowder for 8 rockets, plus the x16 version."""
    src = parse_item(source)
    out = []
    for i, mult in enumerate((1, bulk)):
        n = per * mult
        cost = src.with_count(src.count * mult)
        name = gamedata.load().item_name(src.id)
        q = Q(f"Rockets for {name}" + (f" x{bulk}" if i else ""), [Task("item", item=cost, consume=True)],
              f"{n} firework_rocket", sub="Firework rockets" + (", bulk" if i else ""))
        q.pair = i
        q.auto_desc = lambda ctx, cost=cost, n=n: [f"{ctx.items_text([cost])} = {plural(n, 'rocket')}."]
        out.append(q)
    return out


# =========================================================== layout

class Grid:
    """Rows of `cols` quests, `dx`/`dy` apart. A new section (gun tier) starts a new row after `gap`."""

    def __init__(self, cols=6, dx=1.5, dy=1.5, gap=0.75):
        self.cols, self.dx, self.dy, self.gap = cols, dx, dy, gap

    def place(self, quests):
        x = y = 0.0
        col, section, first = 0, object(), True
        for q in quests:
            if not first and (col >= self.cols or q.section != section):
                col = 0
                y += self.dy + (self.gap if q.section != section else 0)
            section, first = q.section, False
            if q.at is None:
                q.at = (col * self.dx, y)
            col += 1


class Pairs:
    """Single trade on top, bulk trade under it; `cols` pairs per block, blocks `block` apart."""

    def __init__(self, cols=5, dx=1.5, dy=1.5, block=3.5):
        self.cols, self.dx, self.dy, self.block = cols, dx, dy, block

    def place(self, quests):
        n = 0
        for q in quests:
            if q.pair == 1:
                continue
            col, row = n % self.cols, n // self.cols
            if q.at is None:
                q.at = (col * self.dx, row * self.block)
            n += 1
        top = None
        for q in quests:
            if q.pair == 0:
                top = q
            elif q.pair == 1 and q.at is None:
                q.at = (top.at[0], top.at[1] + self.dy)


# =========================================================== chapters

class Chapter:
    def __init__(self, filename, title, group, icon, order, quests, repeat=False, auto=None,
                 layout=None, note=None, sub=None, reward_line=False, extra=None, toast=None):
        # toast: show "quest/task complete" popups. Off by default for repeatable shop chapters.
        self.toast = (not repeat) if toast is None else toast
        self.filename, self.title, self.group, self.icon, self.order = filename, title, group, icon, order
        flat = []
        for q in quests:
            flat.extend(q if isinstance(q, list) else [q])
        self.quests = flat
        self.repeat, self.auto, self.layout, self.note, self.sub = repeat, auto, layout, note, sub
        self.reward_line, self.extra = reward_line, extra or {}


class Context:
    def __init__(self, chapters, names=None):
        self.gd = gamedata.load()
        self.gun_names, self.ammo_names = {}, {}
        for rid, name in (names or {}).items():
            kind, _, rest = rid.partition(":")
            table = self.ammo_names if kind == "ammo" else self.gun_names
            table[_ns(rest, "tacz")] = name
        for ch in chapters:
            for q in ch.quests:
                if hasattr(q, "gun_name"):
                    self.gun_names[q.gun_name[0]] = q.gun_name[1]
                if hasattr(q, "ammo_name"):
                    self.ammo_names[q.ammo_name[0]] = q.ammo_name[1]
        self.chapter = None

    def item_label(self, it):
        if it.kind == "gun":
            return self.gun_names.get(it.ref) or self.gd.tacz_name("gun", it.ref) or it.ref
        if it.kind == "ammo":
            return self.ammo_names.get(it.ref) or self.gd.tacz_name("ammo", it.ref) or it.ref
        if it.kind == "attachment":
            return self.gd.tacz_name("attachment", it.ref) or it.ref
        return self.gd.item_name(it.id)

    def items_text(self, items):
        return " + ".join(f"{it.count}x {self.item_label(it)}" for it in items)

    def price_text(self, q):
        return self.items_text([t.kw["item"] for t in q.tasks if t.kind == "item"])

    def guns_using(self, ammo_id):
        names = [self.gun_names.get(g) or self.gd.tacz_name("gun", g) or g for g in self.gd.guns_using(ammo_id)]
        return sorted(names, key=str.lower)

    def reward_line(self, q):
        guns = [r for r in q.rewards if r.kind == "gun"]
        if not guns:
            return None
        totals = {}
        for r in q.rewards:
            if r.kind == "ammo":
                totals[r.ref] = totals.get(r.ref, 0) + r.count
        text = " and ".join(self.item_label(g) for g in guns)
        if totals:
            text += " with " + " and ".join(f"{n} rounds of {self.item_label(Item('tacz:ammo', 1, None, 'ammo', a))}"
                                            for a, n in totals.items())
        return f"Reward: {text}."


# =========================================================== IDs

class IdStore:
    def __init__(self, path=IDS_FILE):
        self.path = path
        self.ids, self.generated = {}, {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.ids = data.get("ids", {})
            self.generated = data.get("generated", {})
        self.used = set(self.ids.values())
        self.new_keys = []
        self.touched = set()

    def reserve(self, ids):
        self.used.update(ids)

    def get(self, key):
        self.touched.add(key)
        if key in self.ids:
            return self.ids[key]
        # FTB Quests reads IDs as signed 64-bit numbers: anything from 8000000000000000 up is
        # invalid and gets silently replaced in game, so stay in the positive half.
        while True:
            v = "%016X" % random.getrandbits(63)
            if v not in self.used and not v.startswith("0000"):
                break
        self.ids[key] = v
        self.used.add(v)
        self.new_keys.append(key)
        return v

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"ids": dict(sorted(self.ids.items())), "generated": self.generated}, f, indent=1)


def _existing_ids():
    """Every ID already used anywhere in the quest folder, so new ones never collide."""
    found = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if k == "id" and isinstance(x, str) and re.fullmatch(r"[0-9A-Fa-f]{16}", x):
                    found.add(x.upper())
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    for root, _, files in os.walk(gamedata.QUESTS_DIR):
        for f in files:
            if f.endswith(".snbt"):
                try:
                    walk(snbt.load(os.path.join(root, f)))
                except (snbt.SNBTError, OSError):
                    pass
    return found


def _groups():
    data = snbt.load(GROUPS_FILE)
    return {g["title"]: g["id"] for g in data.get("chapter_groups", [])}


# =========================================================== build

def _stacks(item, gd):
    size = gamedata.max_stack(gd, item.id, item.tag)
    n, out = item.count, []
    while n > 0:
        out.append(item.with_count(min(n, size)))
        n -= size
    return out


def build_chapter(ch, ctx, ids, groups):
    gd = ctx.gd
    ctx.chapter = ch
    if ch.group not in groups:
        raise QuestError(f"{ch.filename}: chapter group '{ch.group}' is not in chapter_groups.snbt "
                         f"(have: {', '.join(groups)})")
    if ch.layout:
        ch.layout.place(ch.quests)
    titles = {}
    for q in ch.quests:
        if q.key in titles:
            raise QuestError(f"{ch.filename}: two quests use the key '{q.key}'. Give one a different title or key=")
        titles[q.key] = q
    out_quests = []
    for q in ch.quests:
        qkey = f"{ch.filename}/{q.key}"
        if q.at is None:
            raise QuestError(f"{ch.filename}: quest '{q.title}' has no position (add at=(x, y) or a layout)")
        d = {"id": ids.get("q:" + qkey), "title": esc(q.title),
             "x": Double(float(q.at[0])), "y": Double(float(q.at[1]))}
        desc = lines(q.desc) if q.desc is not None else (q.auto_desc(ctx) if q.auto_desc else [])
        if ch.reward_line and q.auto_desc is None:
            rl = ctx.reward_line(q)
            if rl and rl not in desc:
                desc = desc + [rl]
        desc = [x for x in desc if x is not None]
        if desc:
            d["description"] = [esc(x) for x in desc]
        sub = q.sub
        if sub is None and q.auto_sub:
            sub = q.auto_sub(ctx)
        if sub is None and ch.reward_line:
            guns = [r for r in q.rewards if r.kind == "gun"]
            sub = ctx.item_label(guns[0]) if guns else None
        if sub is None:
            sub = ch.sub
        if sub is not None:
            d["subtitle"] = esc(sub)
        repeat = ch.repeat if q.repeat is None else q.repeat
        if repeat:
            d["can_repeat"] = True
        if q.optional:
            d["optional"] = True
        if q.icon is not None:
            d["icon"] = parse_item(q.icon).icon_nbt()
        deps = []
        for a in q.after:
            if isinstance(a, tuple):
                deps.append(ids.get(f"q:{a[0]}/{a[1]}"))
            elif a in titles:
                deps.append(ids.get(f"q:{ch.filename}/{a}"))
            else:
                raise QuestError(f"{ch.filename}: '{q.title}' depends on '{a}', which is not a quest in this chapter")
        if deps:
            d["dependencies"] = deps
        d["tasks"] = [t.nbt(ids.get(f"t:{qkey}/{i}")) for i, t in enumerate(q.tasks)]
        if not ch.toast:
            d["disable_toast"] = True
            for t in d["tasks"]:
                t["disable_toast"] = True
        rewards, auto = [], q.auto or ch.auto
        for r in q.rewards:
            if isinstance(r, command):
                rewards.append(r.nbt())
                continue
            for st in _stacks(r, gd):
                rd = {"id": None, "item": st.nbt(), "type": "item"}
                if st.count != 1:
                    rd["count"] = st.count
                if auto:
                    rd["auto"] = auto
                rewards.append(rd)
        for i, rd in enumerate(rewards):
            rd["id"] = ids.get(f"r:{qkey}/{i}")
        d["rewards"] = rewards
        d.update(q.extra)
        out_quests.append(d)
    chapter = {
        "default_hide_dependency_lines": False,
        "default_quest_shape": "",
        "filename": ch.filename,
        "group": groups[ch.group],
        "icon": parse_item(ch.icon).icon_nbt(),
        "id": ids.get("ch:" + ch.filename),
        "order_index": ch.order,
        "quest_links": [],
        "quests": out_quests,
        "title": esc(ch.title),
    }
    if not ch.toast:
        chapter["disable_toast"] = True
    chapter.update(ch.extra)
    return chapter


# =========================================================== adopt existing IDs

def adopt(chapters, ids):
    """Copy the IDs from the current chapter files into ids.json, so regenerating keeps everyone's progress."""
    n = 0
    for ch in chapters:
        path = os.path.join(CHAPTERS_DIR, ch.filename + ".snbt")
        if not os.path.exists(path):
            continue
        data = snbt.load(path)
        ids.ids.setdefault("ch:" + ch.filename, data["id"])
        by_title = {}
        for q in data["quests"]:
            by_title.setdefault(q.get("title", "").replace("\\&", "&"), q)
        for q in ch.quests:
            old = by_title.get(q.title)
            if not old:
                continue
            qkey = f"{ch.filename}/{q.key}"
            ids.ids.setdefault("q:" + qkey, old["id"])
            for i, t in enumerate(old.get("tasks", [])):
                ids.ids.setdefault(f"t:{qkey}/{i}", t["id"])
            for i, r in enumerate(old.get("rewards", [])):
                ids.ids.setdefault(f"r:{qkey}/{i}", r["id"])
            n += 1
    ids.used = set(ids.ids.values())
    return n


# =========================================================== CLI

def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run(chapters, books=None, names=None):
    ap = argparse.ArgumentParser(description="Generate the FTB Quests chapter files from the data table.")
    ap.add_argument("--check", action="store_true", help="only show what would change; write nothing")
    ap.add_argument("--diff", action="store_true", help="print a line diff of every change")
    ap.add_argument("--force", action="store_true", help="overwrite chapters that were edited in game")
    ap.add_argument("--only", nargs="+", metavar="CHAPTER", help="only these chapter filenames")
    ap.add_argument("--adopt", action="store_true", help="record IDs from the existing files (first run)")
    ap.add_argument("--no-validate", action="store_true", help="skip the validator after writing")
    args = ap.parse_args()

    book.registry = books or {}
    ids = IdStore()
    ids.reserve(_existing_ids())
    if args.adopt:
        n = adopt(chapters, ids)
        ids.save()
        print(f"Adopted IDs for {n} quests into {os.path.relpath(IDS_FILE, gamedata.INSTANCE)}.")
        return 0

    seen = set()
    for ch in chapters:
        if ch.filename in seen:
            raise QuestError(f"two chapters use the filename '{ch.filename}'")
        seen.add(ch.filename)

    ctx = Context(chapters, names)
    groups = _groups()
    selected = [c for c in chapters if not args.only or c.filename in args.only]
    if args.only:
        missing = set(args.only) - {c.filename for c in selected}
        if missing:
            raise QuestError(f"no chapter called {', '.join(sorted(missing))}")

    changes, blocked = [], []
    for ch in selected:
        text = snbt.dumps(build_chapter(ch, ctx, ids, groups))
        path = os.path.join(CHAPTERS_DIR, ch.filename + ".snbt")
        old = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = f.read().replace("\r\n", "\n")
        if old == text:
            ids.generated[ch.filename] = _sha(text)
            continue
        last = ids.generated.get(ch.filename)
        if old is not None and last and _sha(old) != last and not args.force:
            blocked.append(ch.filename)
            continue
        changes.append((ch, path, old, text))

    # stale chapter files the table doesn't know about
    stray = sorted(f[:-5] for f in os.listdir(CHAPTERS_DIR)
                   if f.endswith(".snbt") and f[:-5] not in {c.filename for c in chapters})

    for ch, path, old, text in changes:
        status = "new" if old is None else "changed"
        if old is not None:
            diff = list(difflib.unified_diff(old.splitlines(), text.splitlines(), lineterm="", n=1))
            added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
            removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
            status += f" (+{added} -{removed} lines)"
        print(f"  {ch.filename:<26} {status}")
        if args.diff and old is not None:
            for l in difflib.unified_diff(old.splitlines(), text.splitlines(), f"{ch.filename} (current)",
                                          f"{ch.filename} (generated)", lineterm="", n=1):
                print("    " + l)
    for b in blocked:
        print(f"  {b:<26} SKIPPED: edited in game since the last generate. Copy the change into "
              f"questgen.py, then run again with --force.")
    for s in stray:
        print(f"  {s:<26} not in the data table (left alone; delete it if it is old)")
    if not changes:
        print("Nothing to change." if not blocked else "")

    if args.check:
        return 1 if changes else 0

    if changes:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        bdir = os.path.join(BACKUP_DIR, stamp)
        os.makedirs(bdir, exist_ok=True)
        for ch, path, old, text in changes:
            if old is not None:
                shutil.copy2(path, bdir)
        for ch, path, old, text in changes:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            ids.generated[ch.filename] = _sha(text)
        print(f"Wrote {len(changes)} chapter(s). Old versions saved in questtools/backups/{stamp}/")
    if ids.new_keys:
        print(f"{len(ids.new_keys)} new ID(s) created.")
    ids.save()

    if changes and not args.no_validate:
        import validate
        print()
        return validate.main([])
    return 0


def main(chapters, books=None, names=None):
    try:
        sys.exit(run(chapters, books, names))
    except (QuestError, snbt.SNBTError) as e:
        print(f"ERROR: {e}")
        sys.exit(2)
