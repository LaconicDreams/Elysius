"""Index of what actually exists in this instance, built by scanning jars and the TaCZ gun packs.

Gives the validator and auditor: valid item / entity / advancement / structure / dimension / stat IDs,
English display names, and TaCZ gun, ammo and attachment data (fire modes, ammo type, magazine size,
ammo stack size). The scan is cached in .gamedata_cache.json and redone when any jar changes.
"""

import json
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.dirname(HERE)
MC_DIR = os.path.join(INSTANCE, "minecraft")
QUESTS_DIR = os.path.join(MC_DIR, "config", "ftbquests", "quests")
CACHE = os.path.join(HERE, ".gamedata_cache.json")
CACHE_VERSION = 10


def _mc_version():
    try:
        with open(os.path.join(INSTANCE, "mmc-pack.json"), encoding="utf-8") as f:
            for c in json.load(f)["components"]:
                if c["uid"] == "net.minecraft":
                    return c["version"]
    except (OSError, KeyError, ValueError):
        pass
    return "1.20.1"


def _client_jar():
    ver = _mc_version()
    prism = os.path.dirname(os.path.dirname(INSTANCE))  # .../PrismLauncher
    p = os.path.join(prism, "libraries", "com", "mojang", "minecraft", ver, f"minecraft-{ver}-client.jar")
    return p if os.path.exists(p) else None


def strip_json_comments(text):
    """TaCZ json files contain // and /* */ comments; drop them without touching strings."""
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\":
                out.append(text[i + 1:i + 2])
                i += 2
                continue
            if c == '"':
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        else:
            out.append(c)
        i += 1
    # trailing commas are tolerated by Gson but not by Python's json
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def _load_json(raw):
    try:
        return json.loads(strip_json_comments(raw.decode("utf-8-sig", "replace")))
    except ValueError:
        return None


class _Source:
    """A jar, zip or folder, read the same way."""

    def __init__(self, path):
        self.path = path
        self.is_dir = os.path.isdir(path)
        self.zip = None if self.is_dir else zipfile.ZipFile(path)

    def names(self):
        if self.zip:
            return [n for n in self.zip.namelist() if not n.endswith("/")]
        out = []
        for root, _, files in os.walk(self.path):
            for f in files:
                out.append(os.path.relpath(os.path.join(root, f), self.path).replace("\\", "/"))
        return out

    def read(self, name):
        if self.zip:
            return self.zip.read(name)
        with open(os.path.join(self.path, name), "rb") as f:
            return f.read()

    def close(self):
        if self.zip:
            self.zip.close()


_ASSET_RE = re.compile(r"^assets/([^/]+)/models/item/(.+)\.json$")
_LANG_RE = re.compile(r"^assets/([^/]+)/lang/en_us\.json$")
_ADV_RE = re.compile(r"^data/([^/]+)/advancements/(.+)\.json$")
_STRUCT_RE = re.compile(r"^data/([^/]+)/worldgen/structure/(.+)\.json$")
_STRUCT_TAG_RE = re.compile(r"^data/([^/]+)/tags/worldgen/structure/(.+)\.json$")
_DIM_RE = re.compile(r"^data/([^/]+)/dimension/(.+)\.json$")
_LOOT_RE = re.compile(r"^data/([^/]+)/loot_tables/(.+)\.json$")
_BLOCKSTATE_RE = re.compile(r"^assets/([^/]+)/blockstates/(.+)\.json$")
_TRIM_RE = re.compile(r"^data/([^/]+)/trim_(pattern|material)/(.+)\.json$")
_PARTICLE_RE = re.compile(r"^assets/([^/]+)/particles/(.+)\.json$")
_SOUND_RE = re.compile(r"^assets/([^/]+)/sounds\.json$")
_BIOME_RE = re.compile(r"^data/([^/]+)/worldgen/biome/(.+)\.json$")
_BIOME_TAG_RE = re.compile(r"^data/([^/]+)/tags/worldgen/biome/(.+)\.json$")
_TACZ_IDX_RE = re.compile(r"^data/([^/]+)/index/(guns|ammo|attachments)/(.+)\.json$")
_TACZ_GUNDATA_RE = re.compile(r"^data/([^/]+)/data/guns/(?:.+/)?(.+)_data\.json$")


def _scan_source(src, idx, strict_items):
    items_models, lang = set(), {}
    for name in src.names():
        m = _ASSET_RE.match(name)
        if m:
            items_models.add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = _BLOCKSTATE_RE.match(name)
        if m:
            idx["blocks"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = _BIOME_RE.match(name)
        if m:
            idx["biomes"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = _BIOME_TAG_RE.match(name)
        if m:
            idx["biome_tags"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = _TRIM_RE.match(name)
        if m:
            idx["trims"].add(f"{m.group(2)}:{m.group(1)}:{m.group(3)}")
            continue
        m = _PARTICLE_RE.match(name)
        if m:
            idx["particles"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = _SOUND_RE.match(name)
        if m:
            data = _load_json(src.read(name))
            if isinstance(data, dict):
                idx["sounds"].update(f"{m.group(1)}:{k}" for k in data)
            continue
        m = _LANG_RE.match(name)
        if m:
            data = _load_json(src.read(name))
            if isinstance(data, dict):
                lang.update({k: v for k, v in data.items() if isinstance(v, str)})
            continue
        for rx, key in ((_ADV_RE, "advancements"), (_STRUCT_RE, "structures"), (_DIM_RE, "dimensions"),
                        (_LOOT_RE, "loot_tables")):
            m = rx.match(name)
            if m:
                idx[key].add(f"{m.group(1)}:{m.group(2)}")
                break
        else:
            m = _STRUCT_TAG_RE.match(name)
            if m:
                idx["structures"].add(f"#{m.group(1)}:{m.group(2)}")
                continue
            m = _TACZ_IDX_RE.match(name)
            if m:
                ns, kind, rid = m.groups()
                data = _load_json(src.read(name)) or {}
                idx["tacz_" + kind][f"{ns}:{rid}"] = {
                    "type": data.get("type"), "stack_size": data.get("stack_size"),
                    "name_key": data.get("name"),
                }
                continue
            m = _TACZ_GUNDATA_RE.match(name)
            if m:
                data = _load_json(src.read(name)) or {}
                bullet = data.get("bullet") or {}
                idx["tacz_gundata"][f"{m.group(1)}:{m.group(2)}"] = {
                    "fire_mode": [str(x).upper() for x in data.get("fire_mode", [])],
                    "ammo": data.get("ammo"),
                    "ammo_amount": data.get("ammo_amount"),
                    "rpm": data.get("rpm"),
                    "damage": bullet.get("damage"),
                    "pellets": bullet.get("bullet_amount", 1),
                }

    idx["items"].update(items_models)
    # lang keys only count as items for namespaces that ship no item models at all
    model_ns = {i.split(":")[0] for i in items_models}
    for k, v in lang.items():
        parts = k.split(".")
        if len(parts) == 3 and parts[0] in ("item", "block"):
            rid = f"{parts[1]}:{parts[2]}"
            idx["names"].setdefault(rid, re.sub("§.", "", v))
            if not strict_items and parts[1] not in model_ns:
                idx["items"].add(rid)
        elif len(parts) == 3 and parts[0] == "entity":
            idx["entities"].add(f"{parts[1]}:{parts[2]}")
            idx["names"].setdefault(f"{parts[1]}:{parts[2]}", v)
        elif len(parts) == 3 and parts[0] == "effect":
            idx["effects"].add(f"{parts[1]}:{parts[2]}")
        elif len(parts) == 3 and parts[0] == "enchantment":
            idx["effects"].add(f"{parts[1]}:{parts[2]}")  # enchantments share the "other registry ids" bucket
        elif len(parts) == 3 and parts[0] == "stat" and parts[1] == "minecraft":
            idx["stats"].add(f"minecraft:{parts[2]}")
        elif k.startswith(("tacz.", "travelersbackpack.")):
            idx["lang"][k] = v


def _sources():
    out = []
    cj = _client_jar()
    if cj:
        out.append(("client", cj))
    mods = os.path.join(MC_DIR, "mods")
    for f in sorted(os.listdir(mods)):
        if f.endswith(".jar"):
            out.append(("mod", os.path.join(mods, f)))
    # global datapacks loaded by Paxi (structures, advancements, dimensions, loot tables defined there)
    paxi = os.path.join(MC_DIR, "config", "paxi", "datapacks")
    if os.path.isdir(paxi):
        for f in sorted(os.listdir(paxi)):
            p = os.path.join(paxi, f)
            if os.path.isdir(p) and os.path.isdir(os.path.join(p, "data")):
                out.append(("datapack", p))
    tacz = os.path.join(MC_DIR, "tacz")
    if os.path.isdir(tacz):
        for f in sorted(os.listdir(tacz)):
            p = os.path.join(tacz, f)
            if os.path.isdir(p) or f.endswith(".zip"):
                out.append(("gunpack", p))
    return out


def _fingerprint(sources):
    fp = [CACHE_VERSION]
    for kind, p in sources:
        if os.path.isdir(p):
            # gun packs: newest mtime of any file inside
            newest = 0
            for root, _, files in os.walk(p):
                for f in files:
                    newest = max(newest, os.path.getmtime(os.path.join(root, f)))
            fp.append([p, newest])
        else:
            st = os.stat(p)
            fp.append([p, st.st_mtime, st.st_size])
    return fp


def _build(sources):
    idx = {k: set() for k in ("items", "entities", "advancements", "structures", "dimensions", "stats",
                              "loot_tables", "blocks", "trims", "particles", "sounds", "biomes", "biome_tags",
                              "effects")}
    idx.update(names={}, lang={}, tacz_guns={}, tacz_ammo={}, tacz_attachments={}, tacz_gundata={}, mods=[])
    idx["dimensions"].update({"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"})
    for kind, p in sources:
        try:
            src = _Source(p)
        except (OSError, zipfile.BadZipFile):
            continue
        try:
            _scan_source(src, idx, strict_items=(kind == "client"))
        finally:
            src.close()
        idx["mods"].append(os.path.basename(p))
    # vanilla sounds.json lives in the launcher's asset store, not in the client jar
    prism = os.path.dirname(os.path.dirname(INSTANCE))
    idx_dir = os.path.join(prism, "assets", "indexes")
    if os.path.isdir(idx_dir):
        for f in sorted(os.listdir(idx_dir), reverse=True):
            try:
                with open(os.path.join(idx_dir, f), encoding="utf-8") as fh:
                    objs = json.load(fh).get("objects", {})
                h = objs.get("minecraft/sounds.json", {}).get("hash")
                if h:
                    with open(os.path.join(prism, "assets", "objects", h[:2], h), encoding="utf-8") as fh:
                        idx["sounds"].update(f"minecraft:{k}" for k in json.load(fh))
                    break
            except (OSError, ValueError):
                continue
    # built-in loot table that has no file
    idx["loot_tables"].add("minecraft:empty")
    return idx


class GameData:
    def __init__(self, idx):
        self.items = set(idx["items"])
        self.entities = set(idx["entities"])
        self.advancements = set(idx["advancements"])
        self.structures = set(idx["structures"])
        self.dimensions = set(idx["dimensions"])
        self.stats = set(idx["stats"])
        self.loot_tables = set(idx.get("loot_tables", []))
        self.blocks = set(idx.get("blocks", []))
        self.trims = set(idx.get("trims", []))
        self.particles = set(idx.get("particles", []))
        self.sounds = set(idx.get("sounds", []))
        self.biomes = set(idx.get("biomes", []))
        self.biome_tags = set(idx.get("biome_tags", []))
        self.effects = set(idx.get("effects", []))
        self.names = idx["names"]
        self.lang = idx["lang"]
        self.guns = idx["tacz_guns"]
        self.ammo = idx["tacz_ammo"]
        self.attachments = idx["tacz_attachments"]
        self.gundata = idx["tacz_gundata"]
        self.has_client = any(n.endswith("-client.jar") for n in idx["mods"])
        self.namespaces = {i.split(":")[0] for i in self.items}

    # ---- lookups
    def gun_modes(self, gun_id):
        return self.gundata.get(gun_id, {}).get("fire_mode", [])

    def gun_ammo(self, gun_id):
        return self.gundata.get(gun_id, {}).get("ammo")

    def gun_mag(self, gun_id):
        return self.gundata.get(gun_id, {}).get("ammo_amount")

    def gun_dps(self, gun_id):
        """Rough damage per second of sustained fire (ignores reloads and headshots).
        TaCZ's bullet damage is already the total for all pellets of a shotgun shell."""
        d = self.gundata.get(gun_id, {})
        try:
            return float(d["damage"]) * float(d["rpm"]) / 60.0
        except (KeyError, TypeError, ValueError):
            return None

    def gun_type(self, gun_id):
        return (self.guns.get(gun_id) or {}).get("type")

    def ammo_stack(self, ammo_id):
        return (self.ammo.get(ammo_id) or {}).get("stack_size") or 64

    def tacz_name(self, kind, rid):
        table = {"gun": self.guns, "ammo": self.ammo, "attachment": self.attachments}[kind]
        key = (table.get(rid) or {}).get("name_key")
        name = self.lang.get(key) if key else None
        return re.sub("§.", "", name).strip() if name else None

    def item_name(self, rid):
        if ":" not in rid:
            rid = "minecraft:" + rid
        if rid in self.names:
            return self.names[rid]
        return rid.split(":")[1].replace("_", " ").title()

    def guns_using(self, ammo_id):
        return sorted(g for g, d in self.gundata.items() if d.get("ammo") == ammo_id)


_cached = None


def load(force=False):
    global _cached
    if _cached and not force:
        return _cached
    sources = _sources()
    fp = _fingerprint(sources)
    idx = None
    if not force and os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("fingerprint") == fp:
                idx = data["index"]
        except (OSError, ValueError, KeyError):
            idx = None
    if idx is None:
        built = _build(sources)
        idx = {k: sorted(v) if isinstance(v, set) else v for k, v in built.items()}
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump({"fingerprint": fp, "index": idx}, f)
    _cached = GameData(idx)
    return _cached


# Vanilla items that do not stack to 64 (only used to warn about oversized reward stacks).
_STACK16 = {"ender_pearl", "snowball", "egg", "bucket", "written_book", "writable_book", "armor_stand",
            "honey_bottle", "oak_sign", "banner"}
_STACK1_PAT = re.compile(r"(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|elytra|shulker_box|"
                         r"_bucket|bow|crossbow|trident|shield|totem|potion|saddle|minecart|boat|music_disc|"
                         r"enchanted_book|book_and_quill|flint_and_steel|shears|fishing_rod|spyglass|"
                         r"modern_kinetic_gun|tacz:attachment|travelersbackpack:)")


def max_stack(gd, item_id, tag=None):
    if item_id == "tacz:ammo" and tag and "AmmoId" in tag:
        return gd.ammo_stack(tag["AmmoId"])
    short = item_id.split(":", 1)[1] if ":" in item_id else item_id
    if item_id.startswith("minecraft:") and (short in _STACK16 or short.endswith("_sign") or short.endswith("_banner")):
        return 16
    if _STACK1_PAT.search(item_id) or (item_id.startswith("travelersbackpack:")):
        return 1
    return 64
