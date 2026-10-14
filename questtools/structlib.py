"""Small toolkit for writing structure .nbt pieces and datapack files from Python.

Coordinates inside a template: x = east, y = up, z = south (same as in game with no rotation).
Positions you never set stay "structure void" (the terrain there is kept).
Every block name is checked against the blockstates found in the installed jars.
"""

import json
import os
import re

import gamedata
import nbt
from nbt import NBTList, STRING
from snbt import Double

DATA_VERSION = 3465  # Minecraft 1.20.1


class BuildError(Exception):
    pass


def _client_jar_path():
    p = gamedata._client_jar()
    if not p:
        raise BuildError("Minecraft client jar not found (needed to read vanilla textures)")
    return p


def _ns(rid):
    return rid if ":" in rid else "minecraft:" + rid


def parse_state(spec):
    """'soul_lantern[hanging=true]' -> ('minecraft:soul_lantern', {'hanging': 'true'})"""
    m = re.match(r"^([a-z0-9_:./-]+)(?:\[(.*)\])?$", spec.strip())
    if not m:
        raise BuildError(f"bad block state '{spec}'")
    props = {}
    if m.group(2):
        for kv in m.group(2).split(","):
            k, v = kv.split("=")
            props[k.strip()] = v.strip()
    return _ns(m.group(1)), props


class Template:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.cells = {}      # (x,y,z) -> (name, props tuple, nbt or None)
        self.entities = []
        self.gd = gamedata.load()

    def _check(self, x, y, z):
        sx, sy, sz = self.size
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            raise BuildError(f"block at {(x, y, z)} is outside the template size {self.size}")

    def set(self, x, y, z, spec, nbt_data=None):
        name, props = parse_state(spec)
        if name not in self.gd.blocks:
            raise BuildError(f"block '{name}' does not exist in this instance")
        self._check(x, y, z)
        self.cells[(x, y, z)] = (name, tuple(sorted(props.items())), nbt_data)

    def fill(self, x1, y1, z1, x2, y2, z2, spec, keep=False):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    if keep and (x, y, z) in self.cells:
                        continue
                    self.set(x, y, z, spec)

    def hollow(self, x1, y1, z1, x2, y2, z2, wall, inside="air"):
        """Box with walls/floor/ceiling of `wall` and `inside` filling the interior."""
        self.fill(x1, y1, z1, x2, y2, z2, wall)
        self.fill(x1 + 1, y1 + 1, z1 + 1, x2 - 1, y2 - 1, z2 - 1, inside)

    def get(self, x, y, z):
        c = self.cells.get((x, y, z))
        return c[0] if c else None

    def jigsaw(self, x, y, z, facing, name, target, pool, final_state="minecraft:air", joint="aligned"):
        """Jigsaw block facing out of the piece: north/south/east/west, or up/down (vertical links use a
        rollable joint so the child piece may take any rotation)."""
        orientation = f"{facing}_north" if facing in ("up", "down") else f"{facing}_up"
        if facing in ("up", "down"):
            joint = "rollable"
        self.set(x, y, z, f"jigsaw[orientation={orientation}]",
                 {"id": "minecraft:jigsaw", "name": name, "target": target, "pool": pool,
                  "final_state": final_state, "joint": joint})

    def chest(self, x, y, z, facing, loot_table):
        self.set(x, y, z, f"chest[facing={facing},type=single,waterlogged=false]",
                 {"id": "minecraft:chest", "LootTable": loot_table})

    def spawner(self, x, y, z, entity):
        self.set(x, y, z, "spawner", {"id": "minecraft:mob_spawner", "SpawnData": {"entity": {"id": entity}}})

    def entity(self, x, y, z, data):
        """Entity at block (x,y,z), standing in the middle of it."""
        if data.get("id") not in self.gd.entities:
            raise BuildError(f"entity '{data.get('id')}' does not exist")
        self._check(x, y, z)
        d = dict(data)
        if "Tags" in d:
            d["Tags"] = NBTList(d["Tags"], STRING)
        self.entities.append({"blockPos": [x, y, z], "pos": NBTList([Double(x + 0.5), Double(float(y)),
                                                                      Double(z + 0.5)]), "nbt": d})

    def to_nbt(self):
        palette, index, blocks = [], {}, []
        for (x, y, z), (name, props, data) in sorted(self.cells.items(), key=lambda c: (c[0][1], c[0][2], c[0][0])):
            key = (name, props)
            if key not in index:
                index[key] = len(palette)
                p = {"Name": name}
                if props:
                    p["Properties"] = dict(props)
                palette.append(p)
            b = {"pos": [x, y, z], "state": index[key]}
            if data:
                b["nbt"] = data
            blocks.append(b)
        return {"size": list(self.size), "entities": NBTList(self.entities, 10), "blocks": blocks,
                "palette": palette, "DataVersion": DATA_VERSION}

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nbt.dump(self.to_nbt(), path)


class Pack:
    """Collects datapack files in memory, then writes them all at once."""

    def __init__(self, ns, description):
        self.ns = ns
        self.files = {}  # relative path -> bytes
        self.files["pack.mcmeta"] = json.dumps({"pack": {"pack_format": 15, "description": description}},
                                               indent=2).encode()

    def json(self, rel, data):
        self.files[rel] = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

    def text(self, rel, text):
        self.files[rel] = (text.strip("\n") + "\n").encode("utf-8")

    def template(self, path, tpl):
        """path like 'ashen_barrow/entrance' -> data/<ns>/structures/ashen_barrow/entrance.nbt"""
        self.files[f"data/{self.ns}/structures/{path}.nbt"] = nbt.dumps(tpl.to_nbt())

    def function(self, path, body):
        self.text(f"data/{self.ns}/functions/{path}.mcfunction", body)

    def write(self, root):
        for rel, data in sorted(self.files.items()):
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(data)
        return len(self.files)


# ------------------------------------------------------------- loot helpers

def item_entry(item, count=None, weight=1, nbt_tag=None, functions=None):
    e = {"type": "minecraft:item", "name": _ns(item), "weight": weight}
    fns = list(functions or [])
    if nbt_tag:
        fns.insert(0, {"function": "minecraft:set_nbt", "tag": nbt_tag})
    if count:
        lo, hi = (count, count) if isinstance(count, int) else count
        fns.append({"function": "minecraft:set_count",
                    "count": lo if lo == hi else {"type": "minecraft:uniform", "min": lo, "max": hi}})
    if fns:
        e["functions"] = fns
    return e


def gun_entry(gun_id, weight=1):
    gd = gamedata.load()
    gid = gun_id if ":" in gun_id else "tacz:" + gun_id
    modes = gd.gun_modes(gid)
    if not modes:
        raise BuildError(f"gun '{gid}' is not in the installed gun packs")
    return item_entry("tacz:modern_kinetic_gun", weight=weight,
                      nbt_tag='{GunId:"%s",GunFireMode:"%s",GunCurrentAmmoCount:0}' % (gid, modes[0]))


def ammo_entry(ammo_id, count, weight=1):
    gd = gamedata.load()
    aid = ammo_id if ":" in ammo_id else "tacz:" + ammo_id
    if aid not in gd.ammo:
        raise BuildError(f"ammo '{aid}' is not in the installed gun packs")
    return item_entry("tacz:ammo", count, weight, '{AmmoId:"%s"}' % aid)


def att_entry(att_id, weight=1):
    gd = gamedata.load()
    aid = att_id if ":" in att_id else "tacz:" + att_id
    if aid not in gd.attachments:
        raise BuildError(f"attachment '{aid}' is not in the installed gun packs")
    return item_entry("tacz:attachment", None, weight, '{AttachmentId:"%s"}' % aid)


def pool(entries, rolls=1, chance=None):
    p = {"rolls": rolls if isinstance(rolls, int) else {"type": "minecraft:uniform", "min": rolls[0], "max": rolls[1]},
         "entries": entries}
    if chance is not None:
        p["conditions"] = [{"condition": "minecraft:random_chance", "chance": chance}]
    return p


def check_items(entries):
    gd = gamedata.load()
    for e in entries:
        if e.get("type") == "minecraft:item" and e["name"] not in gd.items:
            raise BuildError(f"loot item '{e['name']}' does not exist")
