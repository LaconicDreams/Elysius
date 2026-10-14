"""Apply the pack's Neat (health bar) settings and check Jade's HUD settings.

Neat and Jade only write their config files on the first game launch, so:
  1. launch the game once (main menu is enough), quit
  2. run:  py questtools/configure_hud.py            (or --dry-run to only show the changes)

Neat: edits minecraft/config/neat-client.toml in place (comments kept), backs the old file up to
backup/<time>_configure_hud/, re-parses the result with tomllib and checks every value.
Every key below was read from the Neat 1.20.1-41 jar (NeatForgeConfig$ForgeNeatConfig, section "general").
Jade: nothing is changed (its defaults already fit); the script only prints the relevant values.

Exit codes: 0 ok / nothing to do, 1 error, 2 config file not created yet (launch once first).
"""
import datetime
import json
import os
import re
import shutil
import sys
import tomllib

INST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(INST, "minecraft")
NEAT_FILE = os.path.join(GAME, "config", "neat-client.toml")
JADE_DIR = os.path.join(GAME, "config", "jade")

# key -> (jar default, pack value). Section [general].
NEAT_SETTINGS = {
    "max_distance": (24, 24),                         # ~24 blocks (already the default)
    "max_distance_without_line_of_sight": (8, 0),     # 0 = always needs line of sight
    "show_entity_full_health": (True, False),         # bars only on damaged mobs
    "display_on_players": (True, False),
    "display_on_bosses": (True, False),               # hides #forge:bosses and #c:bosses
    "show_on_passive": (True, False),                 # hostile-focused (MobCategory.isFriendly)
    "show_on_hostile": (True, True),
    "only_health_bar_for_target": (False, False),     # Jade already covers the looked-at mob
    "health_bar_height": (4, 3),                      # slim bar
    "background_height": (6, 5),
    "hp_text_height": (14, 10),                       # smaller HP text
    "show_max_hp": (True, False),                     # text is just the current HP
    "show_hp_percentage": (True, False),
    "show_attributes": (True, False),                 # no undead/arthropod icons
    "show_armor": (True, False),                      # no armor icons
}

NEAT_BLACKLIST_DEFAULT = ["minecraft:shulker", "minecraft:armor_stand", "minecraft:cod", "minecraft:salmon",
                          "minecraft:pufferfish", "minecraft:tropical_fish", "minecraft:tadpole"]
# Added to whatever the file already lists (nothing is removed).
NEAT_BLACKLIST_ADD = [
    # bosses that are NOT in #forge:bosses (those are hidden by display_on_bosses = false)
    "alexsmobs:void_worm", "alexsmobs:void_worm_part",
    "minecraft:illusioner",          # Hollow Magus; illusioners never spawn naturally
    # clutter: tiny mobs and multi-part body segments that are LivingEntities
    "minecraft:bat", "alexsmobs:fly", "alexsmobs:cockroach", "alexsmobs:crimson_mosquito",
    "alexsmobs:anaconda_part", "alexsmobs:bone_serpent_part", "alexsmobs:centipede_body", "alexsmobs:centipede_tail",
]


def toml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(json.dumps(x) for x in v) + "]"
    raise TypeError(v)


def verify_entities(ids):
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gamedata
        gd = gamedata.load()
    except Exception as e:  # noqa: BLE001
        print(f"  warning: could not load gamedata ({e}); entity IDs not re-checked")
        return True
    bad = [i for i in ids if i not in gd.entities]
    for b in bad:
        print(f"  ERROR: unknown entity id {b}")
    return not bad


def set_key(text, key, value):
    """Replace `key = ...` inside [general]; handles single- and multi-line arrays. Returns (text, found)."""
    m_sec = re.search(r"(?m)^\s*\[general\]\s*$", text)
    if not m_sec:
        return text, False
    start = m_sec.end()
    m_next = re.search(r"(?m)^\s*\[[^\]]+\]\s*$", text[start:])
    end = start + m_next.start() if m_next else len(text)
    sec = text[start:end]
    m = re.search(rf"(?m)^([ \t]*){re.escape(key)}[ \t]*=[ \t]*", sec)
    if not m:
        return text, False
    vstart = m.end()
    if sec[vstart:vstart + 1] == "[":
        depth, i = 0, vstart
        while i < len(sec):
            c = sec[i]
            if c == '"':
                i = sec.index('"', i + 1)
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        vend = i + 1
    else:
        nl = sec.find("\n", vstart)
        vend = len(sec) if nl < 0 else nl
        # keep a trailing comment if any (night-config does not write one, but be safe)
        line = sec[vstart:vend]
        cm = re.search(r"\s+#.*$", line) if not line.lstrip().startswith('"') else None
        if cm:
            vend = vstart + cm.start()
    sec = sec[:vstart] + toml_value(value) + sec[vend:]
    return text[:start] + sec + text[end:], True


def configure_neat(dry):
    print(f"Neat: {NEAT_FILE}")
    if not os.path.isfile(NEAT_FILE):
        print("  not created yet: launch the game once (main menu is enough), quit, then run this again.")
        return 2
    raw = open(NEAT_FILE, "rb").read()
    text = raw.decode("utf-8")
    try:
        cfg = tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        print(f"  ERROR: cannot parse: {e}")
        return 1
    gen = cfg.get("general")
    if not isinstance(gen, dict):
        print("  ERROR: no [general] section; Neat version changed? Nothing written.")
        return 1
    missing = [k for k in list(NEAT_SETTINGS) + ["blacklist"] if k not in gen]
    if missing:
        print(f"  ERROR: keys not in file (Neat version changed?): {missing}. Nothing written.")
        return 1
    if not verify_entities(NEAT_BLACKLIST_ADD):
        return 1

    wanted = {k: v for k, (_d, v) in NEAT_SETTINGS.items()}
    old_bl = list(gen["blacklist"])
    wanted["blacklist"] = old_bl + [i for i in NEAT_BLACKLIST_ADD if i not in old_bl]

    changes = []
    new = text
    for k, v in wanted.items():
        if gen[k] == v and type(gen[k]) is type(v):
            continue
        new, ok = set_key(new, k, v)
        if not ok:
            print(f"  ERROR: could not locate line for {k}. Nothing written.")
            return 1
        changes.append((k, gen[k], v))
    if not changes:
        print("  already configured, nothing to do.")
        return 0
    for k, o, v in changes:
        print(f"  {k}: {toml_value(o)} -> {toml_value(v)}")
    check = tomllib.loads(new)["general"]
    for k, v in wanted.items():
        if check.get(k) != v:
            print(f"  ERROR: verification failed for {k} ({check.get(k)!r}). Nothing written.")
            return 1
    if dry:
        print("  --dry-run: nothing written.")
        return 0
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    bdir = os.path.join(INST, "backup", f"{ts}_configure_hud")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy2(NEAT_FILE, os.path.join(bdir, "neat-client.toml"))
    with open(NEAT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    tomllib.loads(open(NEAT_FILE, encoding="utf-8").read())
    print(f"  written and re-parsed OK. Old file: {bdir}")
    print("  (Neat reloads client config when the file changes; restart the game if bars do not update.)")
    return 0


def report_jade():
    print(f"Jade: {JADE_DIR} (no changes made; defaults are used)")
    jj = os.path.join(JADE_DIR, "jade.json")
    if not os.path.isfile(jj):
        print("  jade.json not created yet (launch once).")
        return
    try:
        d = json.load(open(jj, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"  could not parse jade.json: {e}")
        return
    ov, ge = d.get("overlay", {}), d.get("general", {})
    for k in ("overlayPosX", "overlayPosY", "overlayAnchorX", "overlayAnchorY", "overlayScale"):
        print(f"  overlay.{k} = {ov.get(k)}")
    print(f"  general.bossBarOverlapMode = {ge.get('bossBarOverlapMode')}")
    pj = os.path.join(JADE_DIR, "plugins.json")
    if os.path.isfile(pj):
        try:
            p = json.load(open(pj, encoding="utf-8"))
            for ns, key in (("minecraft", "entity_health"), ("minecraft", "entity_health.max_for_render"),
                            ("jade", "registry_name"), ("jade", "mod_name")):
                val = p.get(ns, {}).get(key) if isinstance(p.get(ns), dict) else p.get(f"{ns}:{key}")
                print(f"  plugins {ns}:{key} = {val}")
        except Exception as e:  # noqa: BLE001
            print(f"  could not parse plugins.json: {e}")


def main(argv):
    dry = "--dry-run" in argv
    rc = configure_neat(dry)
    report_jade()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
