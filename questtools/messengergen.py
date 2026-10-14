"""
"Der Bote" - the messenger NPC  ->  config/paxi/datapacks/elytra_extras/.../functions/messenger/
                                 +  config/paxi/datapacks/elytra_extras/data/modpack/functions/bote/force_end
                                 +  config/paxi/resourcepacks/elytra_extras_rp (red eyes for ETF, silence, wind)
=====================================================================================================
A wandering trader on a black horse. A quest makes him appear with
    command("/execute as @p at @s run function elytra_extras:messenger/arrive")   (hidden reward)

Script (all texts in CONFIG):
  1. appears, greeting
  2. after a pause: question 1  [JA] [NEIN]
       NEIN -> 1 heart of damage, his eyes turn red, warning + question 2 with only [JA]
       JA (either question) -> eyes normal, the deal
  3. deal: JA -> wish question; NEIN -> the vision ("Seht ihr?" [JA] -> back, deal accepted)
  4. wish chosen -> farewell, he rides off and vanishes in smoke
Clickable answers use /trigger mes_answer; the "Triggered ..." chat line is hidden by switching the
gamerule sendCommandFeedback off while a question is open (restored afterwards / after 60 s).

The scene (CONFIG "scene" ... "wind")
  Every Bote belongs to one player (score mes_owner on horse + trader = the player's mes_pid). Only that
  player sees his lines, gets his buttons, is frozen and hears the music. From the moment he appears until
  he is gone the player has the tag mes_scene:
    * sits on an invisible seat (armor stand, re-mounted every tick), Resistance V + Fire Resistance +
      Water Breathing; blind (except in the vision); the lie damage clears Resistance for that one hit
    * hears Ward (record category) in a loop, stopped while the Bote is angry or the player is in the vision
    * hears a quiet, irregular cave / distant bell layer (not in the vision)
    * the Bote and his horse turn to face the player every tick (not while galloping off)
  Failsafes: relog, death, the Bote missing, or the max scene length (he says the timeout line and leaves)
  release the player. /function modpack:bote/force_end ends every scene at once.
  Wind (AmbientSounds' open-plains wind, played through our own sound event elytra_extras:wind that points at
  the mod's file, so nothing is copied) loops for everyone in the vision and in the Hollow.

Edit CONFIG, then:  py messengergen.py   and in game /reload (F3+T or a restart for sounds / the eye texture).
"""

import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gamedata  # noqa: E402

PACK = os.path.join(gamedata.MC_DIR, "config", "paxi", "datapacks", "elytra_extras")
RP = os.path.join(gamedata.MC_DIR, "config", "paxi", "resourcepacks", "elytra_extras_rp")
FN = "elytra_extras:messenger"
ANGRY_MARK = " "   # invisible no-break space appended to his name while angry (ETF switches the texture)

CONFIG = {
    "name": "Der Bote",
    "greeting": ["Seid gegrüßt. Ein Bad würde euch guttun."],
    "q1": "Ihr seid {player}, richtig?",         # {player} = the name of the player reading it
    "q1_delay_s": 2,
    "lie_damage": 2,                     # health points (2 = 1 heart), magic damage (ignores armour)
    "warning": "Ich warne euch, lügt mich nicht an, es könnte euch alles kosten. "
               "Ich frage euch - Ihr heißt {player}?",
    "deal": "Alleine schafft ihr es keinen Tag zu überleben. Ich biete euch einen Deal an - arbeitet für mich.",
    "deal_no": "Lasst mich euch zeigen wo euer Schicksal liegt ohne mich.",
    "vision_delay_s": 3,                 # blind seconds before the vision
    "vision_text": "Seht ihr?",
    "vision_block": "minecraft:cracked_deepslate_tiles",
    "vision_slots": 8,                   # players in the vision at once get separate blocks (pid % slots)
    "vision_spacing": 1000,              # blocks between those spots (x = slot * spacing)
    # ---------------- step 4: the three wishes (all texts and numbers for the wishes live here)
    "wish_intro": ["Gut. Ich verlange nicht viel. Nur Dinge, die ihr ohnehin tun würdet.",
                   "Sagt mir: Wonach verlangt es euch?"],
    "wish_labels": {"macht": "MACHT", "schutz": "SCHUTZ", "wissen": "WISSEN"},
    "farewell": "Ihr werdet von mir hören.",
    "leave_after_farewell_s": 3,     # after the farewell he gallops off and vanishes
    # every price timer starts only when the scene ends (the Bote is gone)
    "macht": {
        "line": "Macht. Wie vorhersehbar, und doch so selten ehrlich ausgesprochen. Sie sei euer. Doch Macht will "
                "genährt werden: Binnen dreier Tage soll Blut fließen. Ein Dorfbewohner, oder einer euresgleichen. "
                "Ihr entscheidet.",                                  # DRAFT
        "ticks": 72000,               # 3 in-game days to pay (counted while the player is online)
        "remind_at": 24000,           # reminder when this many ticks are left (about 1 day)
        "remind": "Die Zeit läuft, Freund.",                          # DRAFT
        "success": "Das Blut klebt an euren Händen. Und ihr habt es nicht einmal bereut.",   # DRAFT
        "failure": "Ihr habt gezögert. Meine Eintreiber kennen keine Geduld.",              # DRAFT
        "failure_horde": True,        # on failure: a horde (with its usual leader) comes for the player
        "horde_retry_s": 30,          # if no horde spot is found, try again after this long
    },
    "schutz": {
        "line": "Schutz. Der Weg der Vorsichtigen. Ihr sollt ihn haben. Doch wer sich sicher fühlt, wird träge.",  # DRAFT
        "ticks": 12000,               # half an in-game day of Mining Fatigue
        "amplifier": 0,               # 0 = Mining Fatigue I
    },
    "wissen": {
        "line": "Wissen. Ihr wollt sehen, was hinter dem Vorhang liegt? Wer seine Nase in alles steckt, macht sich "
                "Feinde. Ihr werdet sehen.",                          # DRAFT
        "delay_ticks": 3600,          # 3 minutes until the bees come
        "bees": 6,
        "anger_ticks": 24000,         # how long the bees stay angry
        "survive_s": 60,              # alive this long after the bees arrive = "survived"
        "cleanup_s": 120,             # leftover bees are removed after this long
        "arena_range": 128,           # no bees this close to a boss arena (waits until the player has left)
    },
    "trade_hint": "Rechtsklick auf den Boten zum Handeln",    # action bar hint after JA ("" = none)
    "question": "Ist das alles was euer Herz begehrt?",   # after a trade
    "yes": "JA", "no": "NEIN",
    "ask_delay_s": 2,
    "talk_range": 8,                     # trades within this distance count
    "hear_range": 16,                    # AmbientSounds goes quiet within this distance of a Bote
    "spawn_ahead": 3,                    # he appears about this many blocks in front of the player
    "ride_away_s": 2,
    "ride_speed": 0.6,
    "horse_variant": 4,                  # 0 white, 1 creamy, 2 chestnut, 3 brown, 4 black, 5 gray, 6 dark brown
    "facing_eye_height": 2.8,            # his eyes above the horse's feet (used to aim his head at the player)
    # ---------------- the scene: control (frozen, protected, failsafes)
    "scene": {
        "max_s": 600,                    # max scene length; then he says timeout_line and leaves
        "timeout_line": "Die Zeit drängt. Ich muss weiter.",            # DRAFT
        "hard_end_extra_s": 30,          # if he still hasn't left this long after the timeout, release anyway
        "debug_short_s": 30,             # /function ...debug/short sets the max length to this (until /reload)
        "resistance": 4,                 # amplifier 4 = Resistance V = no damage (except the lie damage)
        "seat_y": 0.35,                  # seat height above the feet (a rider sits 0.35 below his seat)
    },
    # ---------------- the scene: sound
    "music": {
        "sound": "minecraft:music_disc.ward",
        "volume": 0.35,                  # quiet; record category (the player's Jukebox/Note Blocks slider)
        "length_ticks": 5030,            # records/ward.ogg is 251.39 s; replayed after this many ticks
        "stop_game_music": True,         # stop the normal background music when Ward starts
    },
    "heartbeat": {                       # optional, while he is angry
        "enabled": False,
        "sound": "minecraft:entity.warden.heartbeat",
        "volume": 0.6,
        "interval_ticks": 20,
    },
    "ambient_layer": {                   # "Höhlen + Glocke", ambient category, not in the vision
        "cave": ("minecraft:ambient.cave", 0.3, 1.0),          # (sound, volume, pitch)
        "bell": ("minecraft:block.bell.resonate", 1.0, 0.5),   # low and far away
        "bell_distance": 8,              # the bell rings this far from the player (random direction)
        "bell_one_in": 3,                # 1 in N sounds is the bell, the rest are cave sounds
        "first_ticks": 200,              # first sound this long after he appears
        "min_ticks": 300,                # then a random pause between min_ticks and min_ticks + range_ticks
        "range_ticks": 600,
    },
    "wind": {                            # AmbientSounds open-plains wind, looped (vision: only this)
        "file": "ambientsounds:wind/light-wind",   # the mod's sound file (event ambientsounds:wind.light-wind)
        "event": "elytra_extras:wind",   # our event for it (no distance fade, so it follows the player)
        "length_ticks": 1200,            # light-wind.ogg is 60.0 s
        "vision_volume": 0.8,
        "hollow_volume": 0.25,           # quiet, under the boss sounds
        "hollow": "elytra_dungeons:the_hollow",
    },
    # chat look
    "name_color": "gold",
    "text_color": "#FFE9A8",
    "voice": ("minecraft:entity.wandering_trader.ambient", 0.7),   # sound with every line
    # trades: (cost item, cost count, result item, result count). "minecraft:id", "ammo:9mm", "kackhaufen"
    "trades": [
        ("kackhaufen", 1, "minecraft:diamond", 1),
        ("minecraft:rotten_flesh", 8, "minecraft:firework_rocket", 16),
        ("minecraft:copper_ingot", 4, "ammo:9mm", 30),
    ],
}

# trigger values
A_TRADE_YES, A_TRADE_NO, A_Q1_YES, A_Q1_NO, A_Q2_YES = 1, 2, 11, 12, 21
A_VISION_YES, A_DEAL_YES, A_DEAL_NO = 31, 41, 42
A_WISH = {"macht": 51, "schutz": 52, "wissen": 53}   # HOOK: later wishes get 54, 55, ... (mes_wish = value - 50)
VISION_DIM = "elytra_extras:vision"
FREEZE_UUID = "1f2e3d4c-5b6a-4978-8695-a4b3c2d1e0f9"
RETURN_DIMS = ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end", "aether:the_aether"]
SCENE_EFFECTS = ["minecraft:blindness", "minecraft:resistance", "minecraft:fire_resistance",
                 "minecraft:water_breathing", "minecraft:jump_boost"]


def item_snbt(spec, count):
    if spec == "kackhaufen":
        with open(os.path.join(PACK, "head_nbt.txt"), encoding="utf-8") as f:
            return '{id:"minecraft:player_head",Count:%db,tag:%s}' % (count, f.read().strip())
    if spec.startswith("ammo:"):
        return '{id:"tacz:ammo",Count:%db,tag:{AmmoId:"tacz:%s"}}' % (count, spec[5:])
    return '{id:"%s",Count:%db}' % (spec, count)


def line(text):
    """A spoken line: blank line, bold name tag, italic text."""
    C = CONFIG
    return json.dumps(["", {"text": f"\n✦ {C['name']} ✦ » ", "color": C["name_color"], "bold": True},
                       {"text": text, "color": C["text_color"], "italic": True, "bold": False}], ensure_ascii=False)


def line_for_player(text):
    """Like line(), but {player} becomes the reading player's own name (send it with execute as ... tellraw @s)."""
    C = CONFIG
    before, _, after = text.partition("{player}")
    parts = ["", {"text": f"\n✦ {C['name']} ✦ » ", "color": C["name_color"], "bold": True},
             {"text": before, "color": C["text_color"], "italic": True, "bold": False}]
    if "{player}" in text:
        parts.append({"selector": "@s", "color": C["text_color"], "italic": True, "bold": False})
        parts.append({"text": after, "color": C["text_color"], "italic": True, "bold": False})
    return json.dumps(parts, ensure_ascii=False)


def buttons(*opts):
    """opts: (label, trigger value, colour)"""
    parts = ["", {"text": "      "}]
    for i, (label, val, col) in enumerate(opts):
        if i:
            parts.append({"text": "     "})
        parts.append({"text": f"[ {label} ]", "color": col, "bold": True,
                      "clickEvent": {"action": "run_command", "value": f"/trigger mes_answer set {val}"},
                      "hoverEvent": {"action": "show_text", "contents": {"text": f"Antworten: {label}", "color": col}}})
    return json.dumps(parts, ensure_ascii=False)


def name_json(angry=False):
    return json.dumps({"text": CONFIG["name"] + (ANGRY_MARK if angry else ""), "color": CONFIG["name_color"]},
                      ensure_ascii=False)


def build():
    C = CONFIG
    gd = gamedata.load()
    for cost, _, res, _ in C["trades"]:
        for spec in (cost, res):
            if spec == "kackhaufen":
                continue
            if spec.startswith("ammo:"):
                if "tacz:" + spec[5:] not in gd.ammo:
                    raise SystemExit(f"ERROR: ammo '{spec}' does not exist")
            elif spec not in gd.items:
                raise SystemExit(f"ERROR: item '{spec}' does not exist")
    sounds = [C["voice"][0], C["music"]["sound"], C["heartbeat"]["sound"], C["ambient_layer"]["cave"][0],
              C["ambient_layer"]["bell"][0], C["wind"]["file"].replace("/", ".", 1)]
    for s in sounds:
        if s not in gd.sounds:
            raise SystemExit(f"ERROR: sound '{s}' does not exist")
    recipes = ",".join(
        "{buy:%s,sell:%s,maxUses:9999,uses:0,rewardExp:0b,xp:0,priceMultiplier:0f,demand:0,specialPrice:0}"
        % (item_snbt(c, cn), item_snbt(r, rn)) for c, cn, r, rn in C["trades"])
    hr, tr = C["hear_range"], C["talk_range"]
    W, S, MU, HB, AM, WI = C["wissen"], C["scene"], C["music"], C["heartbeat"], C["ambient_layer"], C["wind"]
    res = S["resistance"]
    eye = C["facing_eye_height"]
    # every line goes to the player whose scene it is (tag mes_cur); the voice sounds where @s stands
    voice = f"execute at @s run playsound {C['voice'][0]} neutral @a[tag=mes_cur] ~ ~ ~ 1 {C['voice'][1]}"

    def speak(text):
        return f"tellraw @a[tag=mes_cur] {line(text)}\n{voice}"

    horse = ('{Tags:["mes_horse","mes_new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Tame:1b,Variant:%d,'
             'SaddleItem:{id:"minecraft:saddle",Count:1b},Passengers:[{id:"minecraft:wandering_trader",'
             'Tags:["mes_npc","mes_npc_new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,'
             "CustomName:'%s',CustomNameVisible:1b,Offers:{Recipes:[]}}]}" % (C["horse_variant"], name_json()))
    seat = ('{Tags:["mes_seat","mes_seat_new"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,'
            'DisabledSlots:4144959}')
    ride_ticks = int(C["ride_away_s"] * 20)
    gallop = "\n".join(f"execute if score @s mes_t matches {t} run playsound minecraft:entity.horse.gallop "
                       f"neutral @a[distance=..32] ~ ~ ~ 1 1" for t in range(ride_ticks, 0, -6))
    yes_no = lambda y, n: buttons((C["yes"], y, "green"), (C["no"], n, "red"))  # noqa: E731
    slots = range(C["vision_slots"])
    slot_x = lambda k: k * C["vision_spacing"]  # noqa: E731
    f = {}
    f["load"] = f"""
scoreboard objectives add mes_trade minecraft.custom:minecraft.traded_with_villager
scoreboard objectives add mes_last dummy
scoreboard objectives add mes_t dummy
scoreboard objectives add mes_tm dummy
scoreboard objectives add mes_up dummy
scoreboard objectives add mes_stage dummy
scoreboard objectives add mes_answer trigger
scoreboard objectives add mes_pid dummy
scoreboard objectives add mes_vt dummy
scoreboard objectives add mes_wish dummy
scoreboard objectives add mes_price dummy
scoreboard objectives add mes_ptime dummy
scoreboard objectives add mes_pflag dummy
scoreboard objectives add mes_hp dummy
scoreboard objectives add mes_retry dummy
scoreboard objectives add mes_dth deathCount
scoreboard objectives add mes_bt dummy
# the scene (per player): owner link, timers, failsafes
scoreboard objectives add mes_owner dummy
scoreboard objectives add mes_stime dummy
scoreboard objectives add mes_mus dummy
scoreboard objectives add mes_amb dummy
scoreboard objectives add mes_wind dummy
scoreboard objectives add mes_hb dummy
scoreboard objectives add mes_leave minecraft.custom:minecraft.leave_game
scoreboard objectives add mes_sdth deathCount
scoreboard players add #hidden mes_t 0
scoreboard players set #neg mes_t -1
scoreboard players set #4 mes_t 4
scoreboard players set #6 mes_t 6
scoreboard players set #7 mes_t 7
scoreboard players set #8 mes_t 8
scoreboard players set #20 mes_t 20
scoreboard players set #32768 mes_t 32768
scoreboard players set #65536 mes_t 65536
scoreboard players set #lcg mes_t 1103515245
scoreboard players set #slots mes_t {C['vision_slots']}
scoreboard players set #amb_range mes_t {AM['range_ticks']}
scoreboard players set #bell mes_t {AM['bell_one_in']}
scoreboard players set #max mes_stime {S['max_s'] * 20}
execute unless score #rng mes_t matches -2147483648.. store result score #rng mes_t run time query gametime
scoreboard players add #next mes_pid 0
# team: lets AmbientSounds (client side) recognise the Bote and go silent near him (region elytra_bote)
team add mes_bote
""" + "\n".join(f"execute in {VISION_DIM} run forceload add {slot_x(k)} 0" for k in slots) + f"""
data modify storage {FN} offers set value {{Recipes:[{recipes}]}}
schedule function {FN}/loop 10t replace
"""
    hb_line = (f"execute if entity @s[tag=mes_angry,tag=!mes_in_vision] run function {FN}/scene/heartbeat"
               if HB["enabled"] else "# heartbeat: off (CONFIG heartbeat.enabled)")
    f["loop"] = f"""
# every 10 ticks
schedule function {FN}/loop 10t replace
# failsafes first: relog, death, Botes without their player, seats without a scene
execute as @a[scores={{mes_leave=1..}}] run function {FN}/scene/rejoin
execute as @a[scores={{mes_sdth=1..}}] run function {FN}/scene/died
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] run function {FN}/bote_check
execute as @e[type=minecraft:armor_stand,tag=mes_seat] run function {FN}/scene/seat_orphan
# stage 0: greeting done, question 1 after a pause
scoreboard players remove @e[type=minecraft:wandering_trader,tag=mes_npc,scores={{mes_stage=0,mes_t=1..}}] mes_t 1
execute as @e[type=minecraft:wandering_trader,tag=mes_npc,scores={{mes_stage=0,mes_t=..0}}] at @s run function {FN}/ask_q1
# trades (only the scene's own player, near a Bote who is open for business)
scoreboard players add @a mes_trade 0
execute as @a[tag=mes_scene] at @s if entity @e[type=minecraft:wandering_trader,tag=mes_npc,scores={{mes_stage=3}},distance=..{tr}] run function {FN}/check_trade
execute as @a[tag=mes_scene] at @s unless entity @e[type=minecraft:wandering_trader,tag=mes_npc,scores={{mes_stage=3}},distance=..{tr}] run scoreboard players operation @s mes_last = @s mes_trade
execute as @a[tag=!mes_scene] run scoreboard players operation @s mes_last = @s mes_trade
scoreboard players remove @a[scores={{mes_t=1..}}] mes_t 1
execute as @a[tag=mes_wait,scores={{mes_t=..0}}] at @s run function {FN}/ask_trade
# answers
execute as @a[scores={{mes_answer=1..}}] at @s run function {FN}/answer
team join mes_bote @e[type=minecraft:wandering_trader,tag=mes_npc,team=!mes_bote]
# after the farewell: leave after a short pause
scoreboard players remove @e[type=minecraft:horse,tag=mes_dwait,scores={{mes_t=1..}}] mes_t 1
execute as @e[type=minecraft:horse,tag=mes_dwait,scores={{mes_t=..0}}] at @s run function {FN}/wish/leave_now
# the scene: effects, music, ambient layer, time limit, Bote still there
scoreboard players operation #hard mes_stime = #max mes_stime
scoreboard players add #hard mes_stime {S['hard_end_extra_s'] * 20}
execute as @a[tag=mes_scene] at @s run function {FN}/scene/loop
# wind in the vision and the Hollow (everyone there)
execute as @a at @s if dimension {VISION_DIM} run function {FN}/wind/vision
execute as @a at @s if dimension {WI['hollow']} run function {FN}/wind/hollow
execute as @a[tag=mes_wind_on] at @s unless dimension {VISION_DIM} unless dimension {WI['hollow']} run function {FN}/wind/off
# wish prices (per player; timers only run while the player is online)
execute as @a[scores={{mes_price=1}}] at @s run function {FN}/wish/price_tick
execute as @a[scores={{mes_hp=1}}] at @s if dimension minecraft:overworld run function {FN}/wish/macht_horde_try
scoreboard players add @e[type=minecraft:bee,tag=bote_bienen] mes_bt 10
kill @e[type=minecraft:bee,tag=bote_bienen,scores={{mes_bt={W['cleanup_s'] * 20}..}}]
# the vision: blind countdown, and cleanup for anyone who left it some other way (death, /tp)
scoreboard players remove @a[tag=mes_vision_wait,scores={{mes_vt=1..}}] mes_vt 1
execute as @a[tag=mes_vision_wait,scores={{mes_vt=..0}}] at @s run function {FN}/vision_go
execute as @a[tag=mes_in_vision] at @s unless dimension {VISION_DIM} run function {FN}/vision_cleanup
# open questions expire after 60 s; command feedback returns once nobody has an open question
scoreboard players remove @a[tag=mes_asked] mes_tm 1
tag @a[tag=mes_asked,scores={{mes_tm=..0}}] remove mes_asked
execute if score #hidden mes_t matches 1 unless entity @a[tag=mes_asked] run function {FN}/feedback_on
"""
    f["tick"] = f"""
execute as @e[type=minecraft:horse,tag=mes_leaving] at @s run function {FN}/ride_tick
# keep players in the vision on their single block
""" + "\n".join(f"execute in {VISION_DIM} positioned {slot_x(k)}.5 101 0.5 as @a[tag=mes_vs{k},distance=0.3..] "
                f"run tp @s {slot_x(k)}.5 101 0.5" for k in slots) + f"""
# the scene: back onto the seat (shift dismounts), Bote and horse face their player
execute as @e[type=minecraft:player,tag=mes_scene,tag=!mes_in_vision] run function {FN}/scene/seat
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] at @s run function {FN}/face
"""
    f["tag_owner"] = """
# as a Bote (trader or horse): tag his player mes_cur (and #cur mes_pid = that player's id)
scoreboard players operation #cur mes_pid = @s mes_owner
tag @a remove mes_cur
execute as @a[scores={mes_pid=1..}] if score @s mes_pid = #cur mes_pid run tag @s add mes_cur
"""
    f["tag_mine"] = """
# as a player: tag this player's own Bote (the trader) mes_mine
scoreboard players operation #cur mes_pid = @s mes_pid
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] if score @s mes_owner = #cur mes_pid run tag @s add mes_mine
"""
    f["bote_check"] = f"""
# as a Bote (trader): if his player is gone (offline, scene over), he leaves
function {FN}/tag_owner
execute unless entity @a[tag=mes_cur,tag=mes_scene] on vehicle if entity @s[tag=!mes_leaving] at @s run function {FN}/depart
"""
    f["face"] = f"""
# as + at a Bote's horse (every tick): horse and rider turn to their player's eyes
scoreboard players operation #cur mes_pid = @s mes_owner
tag @a remove mes_look
execute as @a[tag=mes_scene,tag=!mes_in_vision,distance=..16] if score @s mes_pid = #cur mes_pid run tag @s add mes_look
execute if entity @a[tag=mes_look] positioned ~ ~{eye} ~ facing entity @a[tag=mes_look,limit=1] eyes run tp @s ~ ~-{eye} ~ ~ ~
tag @s add mes_facing
execute if entity @a[tag=mes_look] on passengers run data modify entity @s Rotation set from entity @e[type=minecraft:horse,tag=mes_facing,limit=1] Rotation
tag @s remove mes_facing
execute if entity @a[tag=mes_look] at @s run tp @s ~ ~ ~ ~ 0
"""
    f["open_question"] = f"""
# the scene's player (mes_cur) may answer
execute unless score #hidden mes_t matches 1 run function {FN}/feedback_off
tag @a[tag=mes_cur] add mes_asked
scoreboard players set @a[tag=mes_cur] mes_tm 120
scoreboard players enable @a[tag=mes_cur] mes_answer
"""
    f["ask_q1"] = f"""
# as + at the Bote
function {FN}/tag_owner
scoreboard players set @s mes_stage 1
execute as @a[tag=mes_cur] run tellraw @s {line_for_player(C['q1'])}
{voice}
tellraw @a[tag=mes_cur] {yes_no(A_Q1_YES, A_Q1_NO)}
function {FN}/open_question
"""
    f["answer"] = f"""
# as + at a player who clicked (values: {A_Q1_YES}/{A_Q1_NO} question 1, {A_Q2_YES} question 2, {A_TRADE_YES}/{A_TRADE_NO} after a trade)
# keep the button active and feedback hidden for 10 s, so double clicks / old buttons stay silent
scoreboard players set @s mes_tm 20
tag @a remove mes_cur
tag @s add mes_cur
function {FN}/tag_mine
execute if score @s mes_answer matches {A_Q1_YES} as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=1}},limit=1] at @s run function {FN}/accept
execute if score @s mes_answer matches {A_Q2_YES} as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=2}},limit=1] at @s run function {FN}/accept
execute if score @s mes_answer matches {A_Q1_NO} if entity @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=1}}] run function {FN}/punish
execute if score @s mes_answer matches {A_Q1_NO} as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=1}},limit=1] at @s run function {FN}/angry
execute if score @s mes_answer matches {A_TRADE_YES} as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function {FN}/depart
execute if score @s mes_answer matches {A_DEAL_YES} as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=4}},limit=1] at @s run function {FN}/accept_deal
execute if score @s mes_answer matches {A_DEAL_NO} if entity @s[tag=!mes_vision_wait,tag=!mes_in_vision] if entity @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=4}}] run function {FN}/refuse
execute if score @s mes_answer matches {A_VISION_YES} if entity @s[tag=mes_in_vision] run function {FN}/vision_return
execute if score @s mes_answer matches 51..59 if entity @s[tag=!mes_has_wish] run function {FN}/wish/pick
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
scoreboard players set @s mes_answer 0
scoreboard players enable @s mes_answer
"""
    f["punish"] = f"""
# as + at the player who lied: 1 heart. Resistance V would block it, so it is lifted for this one hit
effect clear @s minecraft:resistance
damage @s {C['lie_damage']} minecraft:magic
effect give @s minecraft:resistance infinite {res} true
playsound minecraft:entity.wandering_trader.no neutral @s ~ ~ ~ 1 0.6
# one roll of thunder (weather category: not muted near the Bote); the scene keeps the player blind
playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 1 0.8
"""
    f["angry"] = f"""
# as + at the Bote: red eyes (the invisible mark in his name switches the ETF texture), warning, question 2
function {FN}/tag_owner
scoreboard players set @s mes_stage 2
data merge entity @s {{CustomName:'{name_json(angry=True)}'}}
particle minecraft:angry_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 6
tag @a[tag=mes_cur] add mes_angry
execute as @a[tag=mes_cur] run function {FN}/scene/music_off
execute as @a[tag=mes_cur] run tellraw @s {line_for_player(C['warning'])}
{voice}
tellraw @a[tag=mes_cur] {buttons((C['yes'], A_Q2_YES, 'green'))}
function {FN}/open_question
"""
    hint = (f"title @a[tag=mes_cur] actionbar " + json.dumps({"text": C["trade_hint"], "color": "gold"},
                                                            ensure_ascii=False)) if C["trade_hint"] else ""
    f["accept"] = f"""
# as + at the Bote (question 1 answered with JA): eyes normal (the music comes back), then the deal.
# The blindness stays for the whole scene.
function {FN}/tag_owner
scoreboard players set @s mes_stage 4
tag @a[tag=mes_cur] remove mes_angry
data merge entity @s {{CustomName:'{name_json()}'}}
{speak(C['deal'])}
tellraw @a[tag=mes_cur] {yes_no(A_DEAL_YES, A_DEAL_NO)}
function {FN}/open_question
"""
    f["accept_deal"] = f"""
# as + at the Bote: deal accepted -> his player gets the wish question if they have none; else the shop opens
function {FN}/tag_owner
scoreboard players set @s mes_stage 5
# the pact is made (the rank system gives its points for this advancement)
advancement grant @a[tag=mes_cur] only elytra_extras:bote/pakt
execute store result score #nw mes_t if entity @a[tag=mes_cur,tag=!mes_has_wish]
execute if score #nw mes_t matches 0 run function {FN}/open_shop
execute if score #nw mes_t matches 1.. run function {FN}/wish/ask
"""
    f["open_shop"] = f"""
# as + at the Bote: trades unlocked
scoreboard players set @s mes_stage 3
data modify entity @s Offers set from storage {FN} offers
particle minecraft:happy_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 4
{hint}
"""
    f.update(wish_functions(speak))
    f["refuse"] = f"""
# as + at the player who refused the deal (mes_cur): blind (the scene already is), then the vision
{speak(C['deal_no'])}
tag @s add mes_vision_wait
scoreboard players set @s mes_vt {C['vision_delay_s'] * 2}
"""
    ret_dims = "\n".join(
        f"execute if score #found mes_t matches 0 in {d} as @e[type=minecraft:marker,tag=mes_return] "
        f"if score @s mes_pid = #cur mes_pid at @s run function {FN}/return_here" for d in RETURN_DIMS)
    slot_pick = "\n".join(f"execute if score #slot mes_t matches {k} run function {FN}/vision_slot/{k}" for k in slots)
    f["vision_go"] = f"""
# as + at the player: remember the spot, then the vision (one block in the void), frozen in place
tag @s remove mes_vision_wait
execute unless score @s mes_pid matches 1.. run scoreboard players add #next mes_pid 1
execute unless score @s mes_pid matches 1.. run scoreboard players operation @s mes_pid = #next mes_pid
ride @s dismount
summon minecraft:marker ~ ~ ~ {{Tags:["mes_return","mes_newret"]}}
scoreboard players operation @e[type=minecraft:marker,tag=mes_newret,distance=..1,limit=1] mes_pid = @s mes_pid
execute as @e[type=minecraft:marker,tag=mes_newret,distance=..1] at @s run forceload add ~ ~
tag @e[type=minecraft:marker,tag=mes_newret] remove mes_newret
tag @s add mes_in_vision
function {FN}/scene/music_off
scoreboard players operation #slot mes_t = @s mes_pid
scoreboard players operation #slot mes_t %= #slots mes_t
{slot_pick}
effect clear @s minecraft:blindness
attribute @s minecraft:generic.movement_speed modifier add {FREEZE_UUID} mes_freeze -1 multiply
effect give @s minecraft:jump_boost infinite 128 true
execute unless score #hidden mes_t matches 1 run function {FN}/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
tellraw @s {line(C['vision_text'])}
playsound {C['voice'][0]} neutral @s ~ ~ ~ 1 0.5
tellraw @s {buttons((C['yes'], A_VISION_YES, 'green'))}
"""
    for k in slots:
        f[f"vision_slot/{k}"] = f"""
# as the player: vision spot {k} (players in the vision at the same time do not meet)
tag @s add mes_vs{k}
execute in {VISION_DIM} run setblock {slot_x(k)} 100 0 {C['vision_block']}
execute in {VISION_DIM} run tp @s {slot_x(k)}.5 101 0.5 0 10
"""
    f["vision_back"] = f"""
# as a player in the vision: unfreeze, back to the spot they came from (their seat is still there)
function {FN}/vision_cleanup
tag @s add mes_returning
scoreboard players operation #cur mes_pid = @s mes_pid
scoreboard players set #found mes_t 0
{ret_dims}
execute if score #found mes_t matches 0 in minecraft:overworld run spreadplayers 0 0 0 8 false @s
tag @s remove mes_returning
"""
    f["vision_return"] = f"""
# as the player in the vision who answered JA: back to where they stood (still frozen), the deal is accepted
function {FN}/vision_back
function {FN}/tag_mine
execute at @s facing entity @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:wandering_trader,tag=mes_mine,scores={{mes_stage=4}},limit=1] at @s run function {FN}/accept_deal
"""
    f["return_here"] = f"""
# as + at this player's return marker
tp @a[tag=mes_returning,limit=1] ~ ~ ~
forceload remove ~ ~
scoreboard players set #found mes_t 1
kill @s
"""
    f["return_drop"] = """
# as + at a return marker that is no longer needed
forceload remove ~ ~
kill @s
"""
    f["vision_cleanup"] = f"""
# as a player leaving the vision: the vision's own freeze off (the scene seat takes over again)
tag @s remove mes_in_vision
""" + "\n".join(f"tag @s remove mes_vs{k}" for k in slots) + f"""
attribute @s minecraft:generic.movement_speed modifier remove {FREEZE_UUID}
effect clear @s minecraft:jump_boost
"""
    # ------------------------------------------------ the scene
    f["scene/start"] = f"""
# as + at the player the Bote just appeared to: the scene begins (frozen, protected, blind, music)
tag @s add mes_scene
tag @s remove mes_angry
tag @s remove mes_timeout
tag @s remove mes_mus_on
scoreboard players set @s mes_stime 0
scoreboard players set @s mes_mus 0
scoreboard players set @s mes_hb 0
scoreboard players set @s mes_amb {AM['first_ticks']}
scoreboard players set @s mes_leave 0
scoreboard players set @s mes_sdth 0
ride @s dismount
function {FN}/tag_mine
execute facing entity @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] eyes run tp @s ~ ~ ~ ~ ~
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
summon minecraft:armor_stand ~ ~{S['seat_y']} ~ {seat}
scoreboard players operation @e[type=minecraft:armor_stand,tag=mes_seat_new] mes_owner = @s mes_pid
ride @s mount @e[type=minecraft:armor_stand,tag=mes_seat_new,limit=1]
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] remove mes_seat_new
effect give @s minecraft:resistance infinite {res} true
effect give @s minecraft:fire_resistance infinite 0 true
effect give @s minecraft:water_breathing infinite 0 true
effect give @s minecraft:blindness infinite 0 true
"""
    f["scene/seat"] = f"""
# as a player in a scene (every tick): sitting on their own seat? if not, back onto it
scoreboard players set #r mes_t 0
execute on vehicle if entity @s[tag=mes_seat] run scoreboard players set #r mes_t 1
execute if score #r mes_t matches 0 run function {FN}/scene/seat_mount
"""
    f["scene/seat_mount"] = f"""
ride @s dismount
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:armor_stand,tag=mes_seat] if score @s mes_owner = #cur mes_pid run tag @s add mes_myseat
execute unless entity @e[type=minecraft:armor_stand,tag=mes_myseat] at @s run summon minecraft:armor_stand ~ ~{S['seat_y']} ~ {seat}
scoreboard players operation @e[type=minecraft:armor_stand,tag=mes_seat_new] mes_owner = #cur mes_pid
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] add mes_myseat
tag @e[type=minecraft:armor_stand,tag=mes_seat_new] remove mes_seat_new
ride @s mount @e[type=minecraft:armor_stand,tag=mes_myseat,limit=1]
tag @e[type=minecraft:armor_stand,tag=mes_myseat] remove mes_myseat
"""
    f["scene/seat_orphan"] = """
# as a seat: removed when its player is not in a scene any more
scoreboard players operation #cur mes_pid = @s mes_owner
scoreboard players set #n mes_t 0
execute as @a[tag=mes_scene] if score @s mes_pid = #cur mes_pid run scoreboard players set #n mes_t 1
execute if score #n mes_t matches 0 run kill @s
"""
    f["scene/loop"] = f"""
# every 10 ticks, as + at a player in a scene
scoreboard players add @s mes_stime 10
effect give @s minecraft:resistance infinite {res} true
effect give @s minecraft:fire_resistance infinite 0 true
effect give @s minecraft:water_breathing infinite 0 true
execute if entity @s[tag=!mes_in_vision] run effect give @s minecraft:blindness infinite 0 true
# music: Ward while he is calm and the player is not in the vision
execute if entity @s[tag=!mes_angry,tag=!mes_in_vision] run function {FN}/scene/music
execute if entity @s[tag=mes_mus_on,tag=mes_angry] run function {FN}/scene/music_off
execute if entity @s[tag=mes_mus_on,tag=mes_in_vision] run function {FN}/scene/music_off
{hb_line}
execute if entity @s[tag=!mes_in_vision] run function {FN}/scene/ambient
# time limit and "is my Bote still there" (these may end the scene, so they come last)
execute if score @s mes_stime >= #max mes_stime if entity @s[tag=!mes_timeout] run function {FN}/scene/timeout
execute if entity @s[tag=!mes_in_vision] run function {FN}/scene/check_bote
execute if entity @s[tag=mes_scene] if score @s mes_stime >= #hard mes_stime run function {FN}/scene/end
"""
    f["scene/check_bote"] = f"""
scoreboard players operation #cur mes_pid = @s mes_pid
scoreboard players set #n mes_t 0
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] if score @s mes_owner = #cur mes_pid run scoreboard players set #n mes_t 1
execute if score #n mes_t matches 0 run function {FN}/scene/end
"""
    stop_music = "stopsound @s music\n" if MU["stop_game_music"] else ""
    f["scene/music"] = f"""
tag @s add mes_mus_on
scoreboard players remove @s mes_mus 10
execute if score @s mes_mus matches ..0 run function {FN}/scene/music_play
"""
    f["scene/music_play"] = f"""
# Ward for this player only, from the start (a sound cannot resume mid-track)
{stop_music}playsound {MU['sound']} record @s ~ ~ ~ {MU['volume']} 1
scoreboard players set @s mes_mus {MU['length_ticks']}
"""
    f["scene/music_off"] = f"""
stopsound @s record {MU['sound']}
tag @s remove mes_mus_on
scoreboard players set @s mes_mus 0
"""
    f["scene/heartbeat"] = f"""
scoreboard players remove @s mes_hb 10
execute if score @s mes_hb matches ..0 run playsound {HB['sound']} hostile @s ~ ~ ~ {HB['volume']} 1
execute if score @s mes_hb matches ..0 run scoreboard players set @s mes_hb {HB['interval_ticks']}
"""
    cave, bell = AM["cave"], AM["bell"]
    bells = "\n".join(
        f"execute if score #y mes_t matches 0 if score #d mes_t matches {i} rotated {i * 90} 0 positioned "
        f"^ ^ ^{AM['bell_distance']} run playsound {bell[0]} ambient @s ~ ~ ~ {bell[1]} {bell[2]}" for i in range(4))
    f["scene/ambient"] = f"""
scoreboard players remove @s mes_amb 10
execute if score @s mes_amb matches ..0 run function {FN}/scene/ambient_play
"""
    f["scene/ambient_play"] = f"""
# one quiet cave sound or a distant low bell, then a random pause (random numbers: scoreboard LCG + game time)
scoreboard players operation #rng mes_t *= #lcg mes_t
scoreboard players add #rng mes_t 12345
execute store result score #gt mes_t run time query gametime
scoreboard players operation #rng mes_t += #gt mes_t
scoreboard players operation #x mes_t = #rng mes_t
scoreboard players operation #x mes_t /= #65536 mes_t
scoreboard players operation #x mes_t %= #32768 mes_t
scoreboard players operation @s mes_amb = #x mes_t
scoreboard players operation @s mes_amb %= #amb_range mes_t
scoreboard players add @s mes_amb {AM['min_ticks']}
scoreboard players operation #y mes_t = #x mes_t
scoreboard players operation #y mes_t /= #7 mes_t
scoreboard players operation #y mes_t %= #bell mes_t
scoreboard players operation #d mes_t = #x mes_t
scoreboard players operation #d mes_t %= #4 mes_t
execute if score #y mes_t matches 1.. run playsound {cave[0]} ambient @s ~ ~ ~ {cave[1]} {cave[2]}
{bells}
"""
    f["scene/timeout"] = f"""
# as a player whose scene reached the max length: he says the line and leaves
tag @s add mes_timeout
execute if entity @s[tag=mes_in_vision] run function {FN}/vision_back
tag @s remove mes_vision_wait
tag @a remove mes_cur
tag @s add mes_cur
{speak(S['timeout_line'])}
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function {FN}/depart
"""
    f["scene/end"] = f"""
# as a player: the scene is over (Bote gone, relog, death, time limit, force_end) - release everything
tag @s remove mes_scene
scoreboard players operation #cur mes_pid = @s mes_pid
execute if entity @s[tag=mes_in_vision] run function {FN}/vision_back
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:marker,tag=mes_return] if score @s mes_pid = #cur mes_pid at @s run function {FN}/return_drop
tag @s remove mes_vision_wait
ride @s dismount
execute as @e[type=minecraft:armor_stand,tag=mes_seat] if score @s mes_owner = #cur mes_pid run kill @s
""" + "\n".join(f"effect clear @s {e}" for e in SCENE_EFFECTS) + f"""
attribute @s minecraft:generic.movement_speed modifier remove {FREEZE_UUID}
function {FN}/scene/music_off
stopsound @s hostile {HB['sound']}
stopsound @s ambient {cave[0]}
stopsound @s ambient {bell[0]}
tag @s remove mes_angry
tag @s remove mes_timeout
# the wish price starts now (not during the scene)
function {FN}/wish/start_price
# his Bote leaves too, if he is still here
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function {FN}/depart
"""
    f["scene/rejoin"] = f"""
# as a player who logged out and came back: a scene from before is over
scoreboard players set @s mes_leave 0
execute if entity @s[tag=mes_scene] run function {FN}/scene/end
"""
    f["scene/died"] = f"""
scoreboard players set @s mes_sdth 0
execute if entity @s[tag=mes_scene] run function {FN}/scene/end
"""
    # ------------------------------------------------ wind
    for where, vol in (("vision", WI["vision_volume"]), ("hollow", WI["hollow_volume"])):
        f[f"wind/{where}"] = f"""
# as + at a player in the {where}: the wind loop
tag @s add mes_wind_on
scoreboard players remove @s mes_wind 10
execute if score @s mes_wind matches ..0 run playsound {WI['event']} ambient @s ~ ~ ~ {vol} 1
execute if score @s mes_wind matches ..0 run scoreboard players set @s mes_wind {WI['length_ticks']}
"""
    f["wind/off"] = f"""
stopsound @s ambient {WI['event']}
tag @s remove mes_wind_on
scoreboard players set @s mes_wind 0
"""
    f["check_trade"] = f"""
execute unless score @s mes_last matches -2147483648.. run scoreboard players operation @s mes_last = @s mes_trade
execute if score @s mes_trade > @s mes_last run tag @s add mes_wait
execute if score @s mes_trade > @s mes_last run scoreboard players set @s mes_t {C['ask_delay_s'] * 2}
scoreboard players operation @s mes_last = @s mes_trade
"""
    f["ask_trade"] = f"""
# as + at a player who traded
tag @s remove mes_wait
execute unless score #hidden mes_t matches 1 run function {FN}/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
tellraw @s {line(C['question'])}
playsound {C['voice'][0]} neutral @s ~ ~ ~ 1 {C['voice'][1]}
tellraw @s {yes_no(A_TRADE_YES, A_TRADE_NO)}
"""
    f["feedback_off"] = f"""
execute store result score #fb mes_t run gamerule sendCommandFeedback
gamerule sendCommandFeedback false
scoreboard players set #hidden mes_t 1
"""
    f["feedback_on"] = f"""
execute if score #fb mes_t matches 1 run gamerule sendCommandFeedback true
scoreboard players set #hidden mes_t 0
"""
    f["depart"] = f"""
# as + at the Bote's horse: turn around and gallop off
tag @s add mes_leaving
scoreboard players set @s mes_t {ride_ticks}
tp @s ~ ~ ~ ~180 0
playsound minecraft:entity.horse.angry neutral @a[distance=..32] ~ ~ ~ 1 1
"""
    f["ride_tick"] = f"""
tp @s ^ ^ ^{C['ride_speed']}
execute at @s unless block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~1 ~
particle minecraft:cloud ~ ~0.1 ~ 0.3 0 0.3 0.01 2
{gallop}
scoreboard players remove @s mes_t 1
execute if score @s mes_t matches ..0 run function {FN}/vanish
"""
    f["vanish"] = f"""
# as + at the Bote's horse: smoke, gone - and his player's scene ends
tag @s add mes_leaving
particle minecraft:poof ~ ~1.2 ~ 0.7 0.9 0.7 0.05 80 force
particle minecraft:large_smoke ~ ~1.2 ~ 0.6 0.8 0.6 0.02 40 force
playsound minecraft:entity.wandering_trader.disappeared neutral @a[distance=..48] ~ ~ ~ 1.5 0.8
scoreboard players operation #own mes_pid = @s mes_owner
execute as @a[tag=mes_scene] if score @s mes_pid = #own mes_pid run function {FN}/scene/end
execute on passengers run kill @s
tp @s ~ -2000 ~
kill @s
"""
    f["arrive"] = f"""
# as + at the player (quest reward): the Bote appears {C['spawn_ahead']} blocks ahead, on free ground
# (nothing happens while this player already has a Bote scene)
scoreboard players set #up mes_up 0
execute if entity @s[tag=!mes_scene] rotated ~ 0 positioned ^ ^ ^{C['spawn_ahead']} align xz positioned ~0.5 ~ ~0.5 run function {FN}/find
"""
    f["find"] = f"""
execute if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable if block ~ ~2 ~ #minecraft:replaceable run function {FN}/appear
execute if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable if block ~ ~2 ~ #minecraft:replaceable run scoreboard players set #up mes_up 99
scoreboard players add #up mes_up 1
execute if score #up mes_up matches ..24 positioned ~ ~1 ~ run function {FN}/find
"""
    greet = "\n".join(speak(t) for t in C["greeting"])
    f["appear"] = f"""
# as the player, at the free spot: the Bote (owned by this player), then the scene starts
execute unless score @s mes_pid matches 1.. run scoreboard players add #next mes_pid 1
execute unless score @s mes_pid matches 1.. run scoreboard players operation @s mes_pid = #next mes_pid
tag @a remove mes_cur
tag @s add mes_cur
summon minecraft:horse ~ ~ ~ {horse}
scoreboard players operation @e[type=minecraft:horse,tag=mes_new] mes_owner = @s mes_pid
scoreboard players operation @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_owner = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_new,limit=1,sort=nearest,distance=..2] at @s run tp @s ~ ~ ~ facing entity @a[tag=mes_cur,limit=1]
tag @e[type=minecraft:horse,tag=mes_new] remove mes_new
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_stage 0
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_npc_new] mes_t {C['q1_delay_s'] * 2}
team join mes_bote @e[type=minecraft:wandering_trader,tag=mes_npc_new]
tag @e[type=minecraft:wandering_trader,tag=mes_npc_new] remove mes_npc_new
particle minecraft:poof ~ ~1.2 ~ 0.7 0.9 0.7 0.05 60 force
playsound minecraft:entity.wandering_trader.reappeared neutral @a[distance=..48] ~ ~ ~ 1.5 0.8
execute at @s run function {FN}/scene/start
{greet}
"""
    # ------------------------------------------------ tests
    state = json.dumps(["", {"text": "[Bote-Szene] ", "color": "gold"},
                        "Szene ", {"score": {"name": "#s_scene", "objective": "mes_t"}},
                        " | Zeit ", {"score": {"name": "@s", "objective": "mes_stime"}},
                        "/", {"score": {"name": "#max", "objective": "mes_stime"}}, " Ticks",
                        " | Stufe ", {"score": {"name": "#s_stage", "objective": "mes_t"}},
                        " | wütend ", {"score": {"name": "#s_angry", "objective": "mes_t"}},
                        " | Vision ", {"score": {"name": "#s_vision", "objective": "mes_t"}},
                        " | Sitz ", {"score": {"name": "#s_seat", "objective": "mes_t"}},
                        " | Musik ", {"score": {"name": "#s_music", "objective": "mes_t"}},
                        " | Wind ", {"score": {"name": "#s_wind", "objective": "mes_t"}},
                        " | pid ", {"score": {"name": "@s", "objective": "mes_pid"}},
                        " | Wunsch ", {"score": {"name": "#s_wish", "objective": "mes_t"}},
                        " Preis ", {"score": {"name": "#s_price", "objective": "mes_t"}}], ensure_ascii=False)
    f["debug/here"] = f"""
# TEST: /function {FN}/debug/here   the Bote appears in front of you (full script) - same as debug/start
function {FN}/arrive
"""
    f["debug/start"] = f"""
# TEST: start the scene (the Bote appears about {C['spawn_ahead']} blocks in front of you)
function {FN}/arrive
"""
    f["debug/lie"] = f"""
# TEST: jump to the lie: answers question 1 with NEIN right now (damage, red eyes, music stops)
function {FN}/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 1
scoreboard players set @s mes_answer {A_Q1_NO}
function {FN}/answer
"""
    f["debug/vision"] = f"""
# TEST: jump to the vision: answers the deal with NEIN right now
function {FN}/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 4
scoreboard players set @s mes_answer {A_DEAL_NO}
function {FN}/answer
"""
    f["debug/wish"] = f"""
# TEST: jump to the wish choice: answers the deal with JA right now (debug/wish_reset first if you have a wish)
tag @a remove mes_in_vision_dummy
function {FN}/tag_mine
scoreboard players set @e[type=minecraft:wandering_trader,tag=mes_mine] mes_stage 4
scoreboard players set @s mes_answer {A_DEAL_YES}
function {FN}/answer
"""
    f["debug/end"] = f"""
# TEST: end the scene the normal way: your Bote gallops off and vanishes, then you are released
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid at @s run function {FN}/depart
"""
    f["debug/force_end"] = """
# TEST: the operator emergency stop for everyone
function modpack:bote/force_end
"""
    f["debug/short"] = f"""
# TEST: max scene length {S['debug_short_s']} s for every scene (until the next /reload)
scoreboard players set #max mes_stime {S['debug_short_s'] * 20}
tellraw @s {{"text":"Bote: maximale Szenenlänge jetzt {S['debug_short_s']} s (bis /reload)","color":"gray"}}
"""
    f["debug/state"] = f"""
# TEST: your scene state in chat (1 = yes, 0 = no)
execute store success score #s_scene mes_t if entity @s[tag=mes_scene]
execute store success score #s_angry mes_t if entity @s[tag=mes_angry]
execute store success score #s_vision mes_t if entity @s[tag=mes_in_vision]
execute store success score #s_music mes_t if entity @s[tag=mes_mus_on]
execute store success score #s_wind mes_t if entity @s[tag=mes_wind_on]
scoreboard players set #s_seat mes_t 0
execute on vehicle if entity @s[tag=mes_seat] run scoreboard players set #s_seat mes_t 1
scoreboard players set #s_stage mes_t -1
function {FN}/tag_mine
execute as @e[type=minecraft:wandering_trader,tag=mes_mine,limit=1] run scoreboard players operation #s_stage mes_t = @s mes_stage
tag @e[type=minecraft:wandering_trader,tag=mes_mine] remove mes_mine
scoreboard players set #s_wish mes_t 0
scoreboard players set #s_price mes_t 0
execute if score @s mes_wish matches 1.. run scoreboard players operation #s_wish mes_t = @s mes_wish
execute if score @s mes_price matches 1.. run scoreboard players operation #s_price mes_t = @s mes_price
tellraw @s {state}
"""
    f["debug/remove"] = f"""
# TEST: /function {FN}/debug/remove   removes every Bote within 64 blocks (no drops; their scenes end)
execute as @e[type=minecraft:horse,tag=mes_horse,distance=..64] at @s run function {FN}/vanish
"""
    f["debug/wind"] = f"""
# TEST: plays the wind once at vision volume (to check the sound itself works)
playsound {WI['event']} ambient @s ~ ~ ~ {WI['vision_volume']} 1
"""
    # the dummy-tag line above is not needed; keep debug/wish clean
    f["debug/wish"] = f["debug/wish"].replace("tag @a remove mes_in_vision_dummy\n", "")
    return f


def force_end_function():
    return f"""
# OPERATOR: /function modpack:bote/force_end - ends every Bote scene at once: everyone is released,
# every Bote vanishes, seats and return markers are removed
execute as @a[tag=mes_scene] run function {FN}/scene/end
execute as @a[tag=mes_in_vision] run function {FN}/vision_back
execute as @e[type=minecraft:horse,tag=mes_horse] at @s run function {FN}/vanish
execute as @e[type=minecraft:wandering_trader,tag=mes_npc] at @s run tp @s ~ -2000 ~
kill @e[type=minecraft:wandering_trader,tag=mes_npc]
kill @e[type=minecraft:armor_stand,tag=mes_seat]
execute as @e[type=minecraft:marker,tag=mes_return] at @s run function {FN}/return_drop
tellraw @s {{"text":"Bote: alle Szenen beendet.","color":"gray"}}
"""


def wish_functions(speak):
    """Step 4: the three wishes and their prices. Everything per player (scores + tags on the player).
    mes_price: 4 chosen (starts when the scene ends), 1 running, 2 paid/endured/survived, 3 failed."""
    C = CONFIG
    M, S, W = C["macht"], C["schutz"], C["wissen"]
    to_me = lambda text: f"tellraw @s {line(text)}\nplaysound {C['voice'][0]} neutral @s ~ ~ ~ 1 {C['voice'][1]}"  # noqa: E731
    f = {}
    btns = buttons(*[(C["wish_labels"][k], v, col) for (k, v), col in
                     zip(A_WISH.items(), ("red", "aqua", "light_purple"))])
    intro = "\n".join(speak(t) for t in C["wish_intro"])
    f["wish/ask"] = f"""
# as + at the Bote after the deal (mes_cur = his player): the wish question, if they have not chosen yet
{intro}
tellraw @a[tag=mes_cur,tag=!mes_has_wish] {btns}
function {FN}/open_question
"""
    f["wish/pick"] = f"""
# as + at a player who clicked a wish (once per player). mes_wish: 1 Macht, 2 Schutz, 3 Wissen
tag @s add mes_has_wish
scoreboard players operation @s mes_wish = @s mes_answer
scoreboard players remove @s mes_wish 50
scoreboard players set @s mes_pflag 0
scoreboard players set @s mes_hp 0
execute if score @s mes_wish matches 1 run function {FN}/wish/macht
execute if score @s mes_wish matches 2 run function {FN}/wish/schutz
execute if score @s mes_wish matches 3 run function {FN}/wish/wissen
# HOOK: later wishes (mes_wish 4, 5, ...) are dispatched here
# HOOK: everything that comes with the chosen path (path rewards) listens to this function tag
function #modpack:bote/wunsch_gewaehlt
# chosen without a scene (test function): the price starts at once
execute unless entity @s[tag=mes_scene] run function {FN}/wish/start_price
{speak(C['farewell'])}
scoreboard players operation #cur mes_pid = @s mes_pid
execute as @e[type=minecraft:horse,tag=mes_horse,tag=!mes_leaving] if score @s mes_owner = #cur mes_pid run function {FN}/wish/leave_soon
"""
    f["wish/leave_soon"] = f"""
# as the Bote's horse: ride off a few seconds after the farewell
tag @s add mes_dwait
scoreboard players set @s mes_t {C['leave_after_farewell_s'] * 2}
"""
    f["wish/leave_now"] = f"""
tag @s remove mes_dwait
execute if entity @s[tag=!mes_leaving] run function {FN}/depart
"""
    f["wish/macht"] = f"""
{speak(M['line'])}
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_macht
"""
    f["wish/schutz"] = f"""
{speak(S['line'])}
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_schutz
"""
    f["wish/wissen"] = f"""
{speak(W['line'])}
scoreboard players set @s mes_price 4
advancement grant @s only elytra_extras:bote/wish_wissen
"""
    f["wish/start_price"] = f"""
# as a player whose scene just ended: a chosen price (mes_price 4) starts running now
execute if score @s mes_price matches 4 if score @s mes_wish matches 1 run scoreboard players set @s mes_ptime {M['ticks']}
execute if score @s mes_price matches 4 if score @s mes_wish matches 2 run scoreboard players set @s mes_ptime {S['ticks']}
execute if score @s mes_price matches 4 if score @s mes_wish matches 2 run effect give @s minecraft:mining_fatigue infinite {S['amplifier']} true
execute if score @s mes_price matches 4 if score @s mes_wish matches 3 run scoreboard players set @s mes_ptime {W['delay_ticks']}
execute if score @s mes_price matches 4 run scoreboard players set @s mes_price 1
"""
    f["wish/price_tick"] = f"""
# every 10 ticks, as + at a player whose price is open (mes_price 1)
scoreboard players remove @s mes_ptime 10
execute if score @s mes_wish matches 1 run function {FN}/wish/tick_macht
execute if score @s mes_wish matches 2 run function {FN}/wish/tick_schutz
execute if score @s mes_wish matches 3 run function {FN}/wish/tick_wissen
"""
    # ---- Macht
    f["wish/tick_macht"] = f"""
execute if score @s mes_pflag matches 0 if score @s mes_ptime matches ..{M['remind_at']} run function {FN}/wish/macht_remind
execute if score @s mes_ptime matches ..0 run function {FN}/wish/macht_fail
"""
    f["wish/macht_remind"] = f"""
scoreboard players set @s mes_pflag 1
{to_me(M['remind'])}
"""
    horde = (f"scoreboard players set @s mes_hp 1\nscoreboard players set @s mes_retry 0"
             if M["failure_horde"] else "# failure_horde is off")
    f["wish/macht_fail"] = f"""
# price not paid in time
scoreboard players set @s mes_price 3
advancement grant @s only elytra_extras:bote/macht_failed
{to_me(M['failure'])}
{horde}
"""
    f["wish/macht_horde_try"] = f"""
# as + at a player in the overworld who is owed a horde (retried until a valid spot is found)
scoreboard players remove @s[scores={{mes_retry=1..}}] mes_retry 10
execute if score @s mes_retry matches ..0 run function {FN}/wish/macht_horde_start
"""
    f["wish/macht_horde_start"] = f"""
# uses the existing horde system (overworld only, spawn spot rules, leader with its caps / no-repeat rule)
scoreboard players reset @s mh_cd
function modpack:horde/start
execute if score @s mh_cd matches 1.. run scoreboard players set @s mes_hp 0
execute if score @s mes_hp matches 1 run scoreboard players set @s mes_retry {M['horde_retry_s'] * 20}
"""
    f["wish/kill_check"] = f"""
# advancement reward: this player just killed a villager or a player
advancement revoke @s only elytra_extras:bote/kill_villager
advancement revoke @s only elytra_extras:bote/kill_player
execute if score @s mes_wish matches 1 if score @s mes_price matches 1 run function {FN}/wish/macht_paid
"""
    f["wish/macht_paid"] = f"""
scoreboard players set @s mes_price 2
advancement grant @s only elytra_extras:bote/macht_paid
{to_me(M['success'])}
"""
    # ---- Schutz
    f["wish/tick_schutz"] = f"""
# milk or death removed the effect: give it back while the price lasts
execute if score @s mes_ptime matches 1.. unless predicate elytra_extras:messenger/has_fatigue run effect give @s minecraft:mining_fatigue infinite {S['amplifier']} true
execute if score @s mes_ptime matches ..0 run function {FN}/wish/schutz_done
"""
    f["wish/schutz_done"] = """
effect clear @s minecraft:mining_fatigue
scoreboard players set @s mes_price 2
advancement grant @s only elytra_extras:bote/schutz_endured
"""
    # ---- Wissen
    f["wish/tick_wissen"] = f"""
# mes_pflag: 0 waiting, 2 due (waits for overworld, away from boss arenas), 3 bees are out
execute if score @s mes_pflag matches 0 if score @s mes_ptime matches ..0 run scoreboard players set @s mes_pflag 2
execute if score @s mes_pflag matches 2 if dimension minecraft:overworld unless entity @e[type=minecraft:marker,tag=ed_arena,distance=..{W['arena_range']}] run function {FN}/wish/bees_go
execute if score @s mes_pflag matches 3 if score @s mes_dth matches 1.. run function {FN}/wish/wissen_failed
execute if score @s mes_pflag matches 3 if score @s mes_ptime matches ..0 run function {FN}/wish/wissen_done
"""
    f["wish/bees_go"] = f"""
scoreboard players set @s mes_pflag 3
scoreboard players set @s mes_ptime {W['survive_s'] * 20}
scoreboard players set @s mes_dth 0
function {FN}/wish/bees_spawn
"""
    # random direction (8) and distance (10-15): branches with literal numbers (1.20.1 has no macros)
    branches = "\n".join(
        f"execute if score #d mes_t matches {d - 10} if score #a mes_t matches {k} rotated {k * 45} 0 "
        f"positioned ^ ^ ^{d} positioned over motion_blocking_no_leaves positioned ~ ~2 ~ "
        f"run function {FN}/wish/bees_here" for d in range(10, 16) for k in range(8))
    f["wish/bees_spawn"] = f"""
# as + at the player: a swarm 10-15 blocks away on the surface, angry at this player
summon minecraft:marker ~ ~ ~ {{Tags:["mes_rng"]}}
execute store result score #r mes_t run data get entity @e[type=minecraft:marker,tag=mes_rng,limit=1,sort=nearest] UUID[0]
kill @e[type=minecraft:marker,tag=mes_rng]
execute if score #r mes_t matches ..-1 run scoreboard players operation #r mes_t *= #neg mes_t
scoreboard players operation #d mes_t = #r mes_t
scoreboard players operation #d mes_t %= #6 mes_t
scoreboard players operation #a mes_t = #r mes_t
scoreboard players operation #a mes_t /= #6 mes_t
scoreboard players operation #a mes_t %= #8 mes_t
{branches}
playsound minecraft:entity.bee.loop_aggressive hostile @s ~ ~ ~ 1 0.8
"""
    offsets = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0)]
    bees = "\n".join(
        f'summon minecraft:bee ~{dx} ~ ~{dz} {{Tags:["bote_bienen","bote_bee_new"],PersistenceRequired:1b,'
        f'AngerTime:{W["anger_ticks"]}}}\n'
        f"data modify entity @e[type=minecraft:bee,tag=bote_bee_new,limit=1,sort=nearest] AngryAt set from entity @s UUID\n"
        f"tag @e[type=minecraft:bee,tag=bote_bee_new] remove bote_bee_new"
        for dx, dz in (offsets * 10)[:W["bees"]])
    f["wish/bees_here"] = f"""
# as the player, at the swarm spot. AngryAt is copied from the player's own UUID (both are int arrays),
# so every bee hunts exactly this player
{bees}
"""
    f["wish/wissen_failed"] = """
scoreboard players set @s mes_price 3
"""
    f["wish/wissen_done"] = """
scoreboard players set @s mes_price 2
advancement grant @s only elytra_extras:bote/wissen_survived
"""
    # ---- tests
    advs = ["wish_macht", "wish_schutz", "wish_wissen", "macht_paid", "macht_failed", "schutz_endured",
            "wissen_survived"]
    f["debug/wish_reset"] = "\n".join(
        ["# TEST: forget this player's wish and price", "tag @s remove mes_has_wish"]
        + [f"scoreboard players reset @s {o}" for o in ("mes_wish", "mes_price", "mes_ptime", "mes_pflag", "mes_hp",
                                                          "mes_retry")]
        + ["effect clear @s minecraft:mining_fatigue", "kill @e[type=minecraft:bee,tag=bote_bienen]"]
        + [f"advancement revoke @s only elytra_extras:bote/{a}" for a in advs])
    f["debug/wish_scene"] = f"""
# TEST: the wish question right now, without the Bote (his shop will not open; the price starts at once)
tag @a remove mes_cur
tag @s add mes_cur
{intro}
tellraw @s {btns}
execute unless score #hidden mes_t matches 1 run function {FN}/feedback_off
tag @s add mes_asked
scoreboard players set @s mes_tm 120
scoreboard players enable @s mes_answer
"""
    f["debug/wish_fast"] = """
# TEST: the running price timer ends in 20 seconds (Macht: the reminder comes at once)
scoreboard players set @s[scores={mes_price=1}] mes_ptime 400
"""
    f["debug/macht_fail"] = """
# TEST: the Macht deadline passes now
scoreboard players set @s[scores={mes_wish=1,mes_price=1}] mes_ptime 0
"""
    f["debug/bees_now"] = f"""
# TEST: a bee swarm for you right now (works without a wish)
function {FN}/wish/bees_spawn
"""
    f["debug/schutz_clear"] = """
# TEST: removes Mining Fatigue (like milk); while the Schutz price runs it comes back within half a second
effect clear @s minecraft:mining_fatigue
"""
    return f


def wish_files():
    """Advancements (FTB Quests can use them as tasks) and the effect predicate."""
    files = {}
    impossible = {"criteria": {"done": {"trigger": "minecraft:impossible"}}}
    for a in ("pakt", "wish_macht", "wish_schutz", "wish_wissen", "macht_paid", "macht_failed", "schutz_endured",
              "wissen_survived"):
        files[f"advancements/bote/{a}.json"] = impossible
    for a, ent in (("kill_villager", "minecraft:villager"), ("kill_player", "minecraft:player")):
        files[f"advancements/bote/{a}.json"] = {
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": ent}}]}}},
            "rewards": {"function": f"{FN}/wish/kill_check"}}
    files["predicates/messenger/has_fatigue.json"] = {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:mining_fatigue": {}}}}
    return files


def silent_ogg_file():
    """A truly silent 2 s Ogg Vorbis (oggtool.py): codec headers from vanilla random/pop.ogg + empty frames."""
    import glob
    import oggtool
    prism = os.path.dirname(os.path.dirname(gamedata.INSTANCE))
    index = sorted(glob.glob(os.path.join(prism, "assets", "indexes", "*.json")))[-1]
    with open(index, encoding="utf-8") as fh:
        h = json.load(fh)["objects"]["minecraft/sounds/random/pop.ogg"]["hash"]
    with open(os.path.join(prism, "assets", "objects", h[:2], h), "rb") as fh:
        return oggtool.silent_ogg(fh.read(), 2.0)[0]

def resource_pack():
    """Red-eyed variant of the wandering trader texture, chosen by ETF when his name ends with ANGRY_MARK."""
    import pngtool
    with zipfile.ZipFile(gamedata._client_jar()) as z:
        w, h, px = pngtool.read(z.read("assets/minecraft/textures/entity/wandering_trader.png"))
    red = list(px)
    emis = [(0, 0, 0, 0)] * (w * h)
    for (x, y), col in {(9, 14): (255, 120, 120, 255), (14, 14): (255, 120, 120, 255),
                        (10, 14): (255, 20, 20, 255), (13, 14): (255, 20, 20, 255)}.items():
        red[y * w + x] = col
        emis[y * w + x] = col
    d = "assets/minecraft/optifine/random/entity"
    WI = CONFIG["wind"]
    return {
        "pack.mcmeta": json.dumps({"pack": {"pack_format": 15, "description":
                                            "Elytra modpack: Der Bote's red eyes (needs Entity Texture Features)"}},
                                  indent=2).encode(),
        f"{d}/wandering_trader2.png": pngtool.write(w, h, red),
        f"{d}/wandering_trader2_e.png": pngtool.write(w, h, emis),
        # matches "Der Bote" + at least one more character (the invisible mark), never the plain name
        f"{d}/wandering_trader.properties": f"textures.1=2\nname.1=regex:Der Bote.+\n".encode(),
        # AmbientSounds: near the Bote (team mes_bote) an inaudible sound with mute 1 / top priority silences
        # every other AmbientSounds sound (same mechanism the mod uses for the warden).
        # elytra_extras:wind plays AmbientSounds' own wind file (not copied) with a very long attenuation
        # distance, so it does not fade when the player moves away from where it started
        "assets/elytra_extras/sounds.json": json.dumps({
            "silence": {"sounds": [{"name": "elytra_extras:silence"}]},
            WI["event"].split(":")[1]: {"sounds": [{"name": WI["file"], "stream": True,
                                                    "attenuation_distance": 256}]},
        }, indent=2).encode(),
        "assets/elytra_extras/sounds/silence.ogg": silent_ogg_file(),
        "assets/ambientsounds/basic/regions/elytra_bote.json": json.dumps({
            "name": "elytra_bote",
            "entity": {"type": "wandering_trader", "team": "mes_bote",
                       "distance": {"max": CONFIG["hear_range"], "fade": 4}},
            "sounds": [{"name": "silence", "mute": 1, "mute-priority": 100, "fade-volume": 0.2,
                        "files": ["elytra_extras:silence"]}]}, indent=2).encode(),
        # AmbientSounds: no ambience at all in the custom dimensions
        "assets/ambientsounds/basic/dimensions/elytra_silent.json": json.dumps({
            "name": "elytra_silent",
            "dimension-names": ["elytra_dungeons:the_hollow", VISION_DIM],
            "mute": True,
            "biome-selector": {"always": False}}, indent=2).encode(),
    }


def add_to_tag(tag, fn=None, ns="minecraft"):
    """Adds fn to the function tag <ns>:<tag> of the elytra_extras pack, keeping what other generators (rankgen,
    pathgen) put there. fn=None only makes sure the tag exists."""
    p = os.path.join(PACK, "data", ns, "tags", "functions", *f"{tag}.json".split("/"))
    vals = []
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            vals = json.load(fh).get("values", [])
    if fn and fn not in vals:
        vals.append(fn)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"values": vals}, fh, indent=2)


def write_function(base, name, body):
    p = os.path.join(base, *name.split("/")) + ".mcfunction"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:   # UTF-8 without BOM
        fh.write("\n".join(l for l in body.strip("\n").splitlines() if l.strip()) + "\n")


def main():
    files = build()
    out = os.path.join(PACK, "data", "elytra_extras", "functions", "messenger")
    if os.path.isdir(out):
        shutil.rmtree(out)
    for name, body in files.items():
        write_function(out, name, body)
    # operator command in the modpack namespace (only this one file is written there)
    write_function(os.path.join(PACK, "data", "modpack", "functions"), "bote/force_end", force_end_function())
    # the vision dimension: an empty void with the Hollow's End-style sky (own copies, no cross-pack refs).
    # No mood sound: in the vision only the wind plays
    data = os.path.join(PACK, "data", "elytra_extras")
    dims = {
        "dimension_type/vision.json": {
            "ambient_light": 0.05, "bed_works": False, "coordinate_scale": 1.0, "effects": "minecraft:the_end",
            "fixed_time": 18000, "has_ceiling": False, "has_raids": False, "has_skylight": False, "height": 256,
            "infiniburn": "#minecraft:infiniburn_end", "logical_height": 256, "min_y": 0,
            "monster_spawn_block_light_limit": 0, "monster_spawn_light_level": 0, "natural": False,
            "piglin_safe": False, "respawn_anchor_works": False, "ultrawarm": False},
        "worldgen/biome/vision.json": {
            "carvers": {}, "downfall": 0.0,
            "effects": {"fog_color": 1704737, "sky_color": 0, "water_color": 4159204, "water_fog_color": 329011},
            "features": [[] for _ in range(11)], "has_precipitation": False, "spawn_costs": {},
            "spawners": {k: [] for k in ("ambient", "axolotls", "creature", "misc", "monster",
                                         "underground_water_creature", "water_ambient", "water_creature")},
            "temperature": 0.5},
        "dimension/vision.json": {
            "type": "elytra_extras:vision",
            "generator": {"type": "minecraft:flat", "settings": {
                "biome": "elytra_extras:vision", "features": False, "lakes": False,
                "layers": [{"block": "minecraft:air", "height": 1}], "structure_overrides": []}}},
    }
    for rel, d in dims.items():
        p = os.path.join(data, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=2)
    for rel, d in wish_files().items():
        p = os.path.join(data, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=2)
    for tag, fn in (("load", f"{FN}/load"), ("tick", f"{FN}/tick")):
        add_to_tag(tag, fn)
    add_to_tag("bote/wunsch_gewaehlt", ns="modpack")     # hook tag (pathgen adds to it)
    if CONFIG["name"] != "Der Bote":
        print("NOTE: the eye-texture rule in resource_pack() matches 'Der Bote'; update it for the new name")
    if os.path.isdir(RP):
        shutil.rmtree(RP)
    for rel, data in resource_pack().items():
        p = os.path.join(RP, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data)
    print(f"Wrote {len(files)} functions to elytra_extras (messenger), modpack:bote/force_end, "
          f"and elytra_extras_rp")


if __name__ == "__main__":
    main()
