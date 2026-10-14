"""Deep checks for one datapack folder (used by validate.py).

Checks that everything a pack refers to actually exists, either inside the pack itself or in the
installed jars: structures -> template pools -> .nbt pieces -> block states / jigsaw links / chest loot
tables / entities, loot tables -> items / TaCZ NBT / nested loot tables, functions -> functions,
entities, loot tables, advancements, particles, sounds, effects, item ids in NBT, bossbars,
advancements -> parents / icons, tags -> their values.
Command syntax itself can only be checked by the game: after /reload, look for errors in logs/latest.log.
"""

import json
import os
import re

import gamedata
import nbt
import snbt


def _rid(ns, path):
    return f"{ns}:{path}"


class PackIndex:
    def __init__(self, root):
        self.root = root
        self.res = {k: {} for k in ("structures_nbt", "template_pool", "processor_list", "structure", "structure_set",
                                    "loot_tables", "functions", "advancements", "tags_functions", "tags_biome",
                                    "dimension", "dimension_type", "biome")}
        data = os.path.join(root, "data")
        if not os.path.isdir(data):
            return
        for ns in os.listdir(data):
            base = os.path.join(data, ns)
            for dirpath, _, files in os.walk(base):
                for fn in files:
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, base).replace("\\", "/")
                    kind, key = self._classify(rel)
                    if kind:
                        self.res[kind][_rid(ns, key)] = p

    @staticmethod
    def _classify(rel):
        rules = [(r"^structures/(.+)\.nbt$", "structures_nbt"),
                 (r"^worldgen/template_pool/(.+)\.json$", "template_pool"),
                 (r"^worldgen/processor_list/(.+)\.json$", "processor_list"),
                 (r"^worldgen/structure/(.+)\.json$", "structure"),
                 (r"^worldgen/structure_set/(.+)\.json$", "structure_set"),
                 (r"^loot_tables/(.+)\.json$", "loot_tables"),
                 (r"^functions/(.+)\.mcfunction$", "functions"),
                 (r"^advancements/(.+)\.json$", "advancements"),
                 (r"^tags/functions/(.+)\.json$", "tags_functions"),
                 (r"^tags/worldgen/biome/(.+)\.json$", "tags_biome"),
                 (r"^dimension/(.+)\.json$", "dimension"),
                 (r"^dimension_type/(.+)\.json$", "dimension_type"),
                 (r"^worldgen/biome/(.+)\.json$", "biome")]
        for rx, kind in rules:
            m = re.match(rx, rel)
            if m:
                return kind, m.group(1)
        return None, None


def check_pack(rep, root, name, check_item):
    gd = gamedata.load()
    idx = PackIndex(root)
    R = idx.res
    where_of = lambda p: f"{name}: {os.path.relpath(p, root)}".replace("\\", "/")  # noqa: E731

    def load_json(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def loot_exists(t):
        return t in R["loot_tables"] or t in gd.loot_tables

    # ---------------- dimensions
    vanilla_dims = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"}
    known_dims = vanilla_dims | gd.dimensions | set(R["dimension"])
    for did, p in R["dimension"].items():
        d = load_json(p)
        t = d.get("type")
        if t not in R["dimension_type"] and t not in ("minecraft:overworld", "minecraft:the_nether", "minecraft:the_end",
                                                      "minecraft:overworld_caves"):
            rep.error(where_of(p), f"dimension type '{t}' does not exist")
        gen = d.get("generator", {})
        biome = (gen.get("settings") or {}).get("biome") if isinstance(gen.get("settings"), dict) else None
        biome = biome or (gen.get("biome_source") or {}).get("biome")
        if biome and biome not in R["biome"] and biome not in gd.biomes:
            rep.error(where_of(p), f"biome '{biome}' does not exist")
    for bid, p in R["biome"].items():
        d = load_json(p)
        for k in ("has_precipitation", "temperature", "downfall", "effects", "spawners", "spawn_costs",
                  "carvers", "features"):
            if k not in d:
                rep.error(where_of(p), f"biome is missing required field '{k}'")
    gd_biomes = gd.biomes | set(R["biome"])

    # ---------------- worldgen
    for sid, p in R["structure"].items():
        d = load_json(p)
        sp = d.get("start_pool")
        if sp and sp not in R["template_pool"] and sp.split(":")[0] == sid.split(":")[0]:
            rep.error(where_of(p), f"start_pool '{sp}' does not exist")
        b = d.get("biomes", "")
        if isinstance(b, str) and b.startswith("#"):
            t = b[1:]
            if t not in R["tags_biome"] and t not in gd.biome_tags:
                rep.error(where_of(p), f"biome tag '{b}' does not exist")
        for k in ("project_start_to_heightmap",):
            if k in d and d[k] not in ("WORLD_SURFACE_WG", "WORLD_SURFACE", "OCEAN_FLOOR_WG", "OCEAN_FLOOR",
                                       "MOTION_BLOCKING", "MOTION_BLOCKING_NO_LEAVES"):
                rep.error(where_of(p), f"{k} '{d[k]}' is not a heightmap type")
        if d.get("max_distance_from_center", 0) > 128:
            rep.error(where_of(p), "max_distance_from_center must be at most 128 in 1.20.1")
    for sid, p in R["structure_set"].items():
        for e in load_json(p).get("structures", []):
            s = e.get("structure", "")
            if s.split(":")[0] == sid.split(":")[0] and s not in R["structure"]:
                rep.error(where_of(p), f"structure '{s}' does not exist")
    pool_pieces = {}
    for pid, p in R["template_pool"].items():
        d = load_json(p)
        pool_pieces[pid] = []
        for e in d.get("elements", []):
            el = e.get("element", {})
            loc = el.get("location")
            if loc:
                pool_pieces[pid].append(loc)
                if loc not in R["structures_nbt"]:
                    rep.error(where_of(p), f"piece '{loc}' has no .nbt file")
            proc = el.get("processors")
            if isinstance(proc, str) and proc != "minecraft:empty" and proc not in R["processor_list"] \
                    and proc.split(":")[0] == pid.split(":")[0]:
                rep.error(where_of(p), f"processor list '{proc}' does not exist")
    for t, p in R["tags_biome"].items():
        for v in load_json(p).get("values", []):
            required = True
            if isinstance(v, dict):
                required, v = v.get("required", True), v.get("id")
            ok = (v[1:] in gd.biome_tags or v[1:] in R["tags_biome"]) if v.startswith("#") else v in gd_biomes
            if not ok:
                (rep.error if required else rep.info)(where_of(p), f"biome '{v}' not found"
                                                     + ("" if required else " (optional, ignored by the game)"))

    # ---------------- structure pieces
    jig_names = {}
    pieces = {}
    for sid, p in R["structures_nbt"].items():
        try:
            d = nbt.load(p)
        except Exception as e:  # noqa: BLE001
            rep.error(where_of(p), f"cannot read NBT: {e}")
            continue
        pieces[sid] = d
        if d.get("DataVersion", 0) > 3465:
            rep.warn(where_of(p), f"DataVersion {d.get('DataVersion')} is newer than 1.20.1 (3465)")
        jig_names[sid] = set()
        for pal in d.get("palette", []):
            if pal.get("Name") not in gd.blocks:
                rep.error(where_of(p), f"block '{pal.get('Name')}' does not exist")
        for b in d.get("blocks", []):
            data = b.get("nbt")
            if not data:
                continue
            if data.get("id") == "minecraft:jigsaw":
                jig_names[sid].add(data.get("name"))
            lt = data.get("LootTable")
            if lt and not loot_exists(lt):
                rep.error(where_of(p), f"chest loot table '{lt}' does not exist")
            se = (data.get("SpawnData") or {}).get("entity", {}).get("id")
            if se and se not in gd.entities:
                rep.error(where_of(p), f"spawner entity '{se}' does not exist")
        for e in d.get("entities", []):
            eid = e.get("nbt", {}).get("id")
            if eid not in gd.entities:
                rep.error(where_of(p), f"entity '{eid}' does not exist")
    for sid, d in pieces.items():
        p = R["structures_nbt"][sid]
        for b in d.get("blocks", []):
            data = b.get("nbt") or {}
            if data.get("id") != "minecraft:jigsaw":
                continue
            pl, target = data.get("pool"), data.get("target")
            if pl in (None, "minecraft:empty"):
                continue
            if pl not in R["template_pool"]:
                if pl.split(":")[0] == sid.split(":")[0]:
                    rep.error(where_of(p), f"jigsaw at {b['pos']} uses pool '{pl}', which does not exist")
                continue
            if not any(target in jig_names.get(loc, set()) for loc in pool_pieces.get(pl, [])):
                rep.error(where_of(p), f"jigsaw at {b['pos']} wants target '{target}', but no piece in pool "
                                       f"'{pl}' has a jigsaw named that, so nothing will attach")

    # ---------------- loot tables
    def walk_entry(e, p):
        t = e.get("type")
        if t == "minecraft:item":
            name = e.get("name")
            if name not in gd.items:
                rep.error(where_of(p), f"loot item '{name}' does not exist")
                return
            for fn in e.get("functions", []):
                if fn.get("function") == "minecraft:set_nbt":
                    try:
                        tag = snbt.loads(fn.get("tag", "{}"))
                    except snbt.SNBTError as ex:
                        rep.error(where_of(p), f"bad NBT on {name}: {ex}")
                        continue
                    check_item(rep, gd, _Src(where_of(p)), None, {"id": name, "tag": tag}, "loot entry")
        elif t == "minecraft:loot_table":
            if not loot_exists(e.get("name")):
                rep.error(where_of(p), f"nested loot table '{e.get('name')}' does not exist")
        for c in e.get("children", []):
            walk_entry(c, p)

    for lid, p in R["loot_tables"].items():
        for pl in load_json(p).get("pools", []):
            for e in pl.get("entries", []):
                walk_entry(e, p)

    # ---------------- advancements
    for aid, p in R["advancements"].items():
        d = load_json(p)
        par = d.get("parent")
        if par and par not in R["advancements"] and par.split(":")[0] == aid.split(":")[0]:
            rep.error(where_of(p), f"parent advancement '{par}' does not exist")
        icon = ((d.get("display") or {}).get("icon") or {}).get("item")
        if icon and icon not in gd.items:
            rep.error(where_of(p), f"icon item '{icon}' does not exist")

    # ---------------- functions
    bossbars_added, bossbars_used = set(), {}
    # functions from the other global (Paxi) datapacks may be called too
    other_functions = set()
    paxi = os.path.dirname(root)
    for other in os.listdir(paxi):
        if os.path.join(paxi, other) != root and os.path.isdir(os.path.join(paxi, other, "data")):
            other_functions |= set(PackIndex(os.path.join(paxi, other)).res["functions"])
    # sound events defined by the global (Paxi) resource packs (assets/<ns>/sounds.json)
    rp_sounds = set()
    rp_root = os.path.join(os.path.dirname(paxi), "resourcepacks")
    for rp in (os.listdir(rp_root) if os.path.isdir(rp_root) else []):
        assets = os.path.join(rp_root, rp, "assets")
        for ns in (os.listdir(assets) if os.path.isdir(assets) else []):
            sj = os.path.join(assets, ns, "sounds.json")
            if os.path.isfile(sj):
                rp_sounds |= {f"{ns}:{k}" for k in load_json(sj)}
    for t, p in R["tags_functions"].items():
        for v in load_json(p).get("values", []):
            if isinstance(v, dict):              # {"id": ..., "required": false} may be missing on purpose
                if v.get("required", True) is False:
                    continue
                v = v.get("id")
            if v not in R["functions"]:
                rep.error(where_of(p), f"function tag lists '{v}', which does not exist")
    patterns = [
        (r"\bfunction (#?[a-z0-9_.-]+:[a-z0-9_/.-]+)", "function"),
        (r"\bsummon ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "entity"),
        (r"\bloot (?:spawn|give|insert|replace)\b.*?\bloot ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "loot"),
        (r'LootTable:"([a-z0-9_.-]+:[a-z0-9_/.-]+)"', "loot"),
        (r'DeathLootTable:"([a-z0-9_.-]+:[a-z0-9_/.-]+)"', "loot"),
        (r"\badvancement (?:grant|revoke) \S+ (?:only|from|until|through) ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "advancement"),
        (r"\bparticle ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "particle"),
        (r"\bplaysound ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "sound"),
        (r"\beffect give \S+ ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "effect"),
        (r'\bid:"([a-z0-9_.-]+:[a-z0-9_/.-]+)"', "id"),
        (r"\bsetblock \S+ \S+ \S+ ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "block"),
        (r"\b(?:type|tag)=[!]?([a-z0-9_.-]+:[a-z0-9_/.-]+)", "selector_type"),
        (r"\b(?:in|if dimension|unless dimension) ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "dimension"),
        (r"\bplace template ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "template"),
        (r"\b(?:effect clear \S+|effect give \S+) ([a-z0-9_.-]+:[a-z0-9_/.-]+)", "effect"),
    ]
    for fid, p in R["functions"].items():
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if text.startswith("﻿"):
            rep.error(where_of(p), "file starts with a UTF-8 BOM (Windows PowerShell 'Set-Content -Encoding utf8' "
                                   "adds one); Minecraft can't parse line 1 and the whole function fails to load. "
                                   "Save it as UTF-8 without BOM")
            text = text[1:]
        lines = text.splitlines()
        for n, line in enumerate(lines, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            w = f"{where_of(p)}:{n}"
            if s.startswith("/"):
                rep.error(w, "commands in .mcfunction files must not start with '/'")
            if s.count("{") != s.count("}") or s.count("[") != s.count("]"):
                rep.error(w, "unbalanced { } or [ ] on this line")
            # commands that accept exactly one entity: a selector that can match several fails to load
            single_rx = (r"\bdamage (@[ae](?:\[[^\]]*\])?)",
                         r"\bdata (?:get|merge|modify|remove) entity (@[ae](?:\[[^\]]*\])?)",
                         r"\bstore (?:result|success) entity (@[ae](?:\[[^\]]*\])?)",
                         r"\bride (@[ae](?:\[[^\]]*\])?)",
                         r"\bride \S+ mount (@[ae](?:\[[^\]]*\])?)",
                         r"\bfacing entity (@[ae](?:\[[^\]]*\])?)",
                         r"\bdamage \S+ \S+ \S+ by (@[ae](?:\[[^\]]*\])?)")
            for rx in single_rx:
                for m in re.finditer(rx, s):
                    if "limit=1" not in m.group(1):
                        rep.error(w, f"'{m.group(1)}' can match more than one entity here, but this command "
                                     f"only accepts one (add limit=1 or use @s); the whole function would fail "
                                     f"to load")
            if re.match(r"(execute .* run )?scale ", s):
                mods_dir = os.path.join(gamedata.MC_DIR, "mods")
                if not any(f.lower().startswith("pehkui") for f in os.listdir(mods_dir)):
                    rep.error(w, "uses the Pehkui /scale command but Pehkui is not in mods/ (the game would "
                                 "refuse to load this function)")
            for rx, kind in patterns:
                for m in re.finditer(rx, s):
                    v = m.group(1)
                    ok = {
                        "function": lambda v: (v[1:] in R["tags_functions"]) if v.startswith("#") else
                        (v in R["functions"] or v in other_functions),
                        "entity": lambda v: v in gd.entities,
                        "loot": loot_exists,
                        "advancement": lambda v: v in R["advancements"] or v in gd.advancements,
                        "particle": lambda v: v in gd.particles,
                        "sound": lambda v: v in gd.sounds or v in rp_sounds,
                        "effect": lambda v: v in gd.effects,
                        "id": lambda v: v in gd.items or v in gd.entities or v in gd.effects,
                        "block": lambda v: v in gd.blocks,
                        "selector_type": lambda v: v in gd.entities if "type=" in m.group(0) else True,
                        "dimension": lambda v: v in known_dims,
                        "template": lambda v: v in R["structures_nbt"],
                    }[kind](v)
                    if not ok:
                        rep.error(w, f"{kind.replace('_', ' ')} '{v}' does not exist")
            m = re.match(r"bossbar add (\S+)", s)
            if m:
                bossbars_added.add(m.group(1))
            m = re.match(r"(?:execute .*run )?bossbar set (\S+)", s) or re.search(r"store result bossbar (\S+)", s)
            if m:
                bossbars_used.setdefault(m.group(1), w)
    for b, w in bossbars_used.items():
        if b not in bossbars_added:
            rep.error(w, f"bossbar '{b}' is used but never created with 'bossbar add'")
    return {k: len(v) for k, v in R.items()}


class _Src:
    def __init__(self, w):
        self.rel = w

    def where(self, *_):
        return self.rel
