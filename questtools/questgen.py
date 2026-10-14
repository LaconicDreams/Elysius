"""
Elytra modpack quest generator
==============================
Every FTB Quests chapter is defined in the table below. Edit a line, then run:

    py questgen.py            write the chapter files (old ones are backed up, then the validator runs)
    py questgen.py --check    show which chapters would change, write nothing
    py questgen.py --diff     same as a normal run, but also print every changed line
    py questgen.py --only gun_shop rockets      only rebuild those chapters

IDs, '&' escaping, stack splitting and the price / reward text are handled for you.
Quests are matched to their saved IDs by title, so renaming a quest in this file gives it a new ID
(players lose progress on that quest). To rename safely, keep the old name as the key:
    Q("New Name", ..., key="Old Name")

QUICK REFERENCE
---------------
Items (comma-separated; a count in front, "minecraft:" can be left out):
    "6 gold_ingot"      "aether:zanite_gemstone"     "64 rocket"  (= firework_rocket)
    "gun:glock_17"      gun, first fire mode of that gun     "gun:db_short@BURST"   pick the fire mode
    "gun:m1911 loaded"  full magazine + round in the chamber
    "60 ammo:9mm"       "att:sight_552"              "elytra{Damage:0,Unbreakable:1b}"  raw NBT
    book("iron")        a written book from BOOKS    named("red_shulker_box", "Hero's Box")
    Rewards larger than a stack (e.g. 150 ammo) are split into stacks automatically.

Tasks:
    "give 6 gold_ingot"  takes the items     "have 6 gold_ingot"  only checks for them
    "kill zombie 10"     "kill aether:slider 1"
    "fly 25km"           "playtime 10h"      "stat mob_kills 250"
    "adv story/smelt_iron"   "dim the_nether"   "structure pillager_outpost"   "check"
    Several tasks: "give 2 gunpowder; give 2 iron_ingot"

Quest rows:
    Q(title, task, reward, desc="text" or ["line 1", "line 2"], sub="subtitle", at=(x, y),
      after="Other quest title" or [...], icon="gun:ak47", optional=True, repeat=True)
    gun(gun_id, name, price, tier, mode="AUTO")      one gun shop entry
    ammo(ammo_id, name, price, per=rounds)           single trade + a bulk trade for one full stack
    att(attachment_id, name, price)                  one attachment trade
    rockets(item, per)                               single + x16 rocket trade
    Prices: "12 iron_ingot + 5 gold_ingot"
    Shop descriptions, ammo "Fits:" lists and bounty "Reward:" lines are written for you.

Text: '&' is always shown as a literal '&'. For colours use the section sign, e.g. "§cRed".
"""

from questlib import Chapter, Grid, Pairs, Q, ammo, att, book, command, gun, main, named, rockets

ATT_NOTE = "Hold a gun and press Z to fit it in the attachment screen."

# The "Kackhaufen" decoration head (recipe in config/paxi/datapacks/elytra_extras); same NBT as the recipe result.
import os as _os
KACKHAUFEN = "player_head" + open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "minecraft", "config", "paxi",
                                                "datapacks", "elytra_extras", "head_nbt.txt"), encoding="utf-8").read().strip()

# Display names for TaCZ things that are not sold in a shop below (shop rows name themselves).
NAMES = {
    "gun:taurus943": "Taurus 943",
}

# Written books (pages are plain text; each list entry is one page)
BOOKS = {
    'the_dark_sun': dict(
        title='Logbook: The Dark Sun', author='Courier Mara Venn',
        pages=[
            'If you are reading this, the wings chose you. I am sorry. The sun went dark the day the skyways fell, and the beacons went out one by one.',
            'Follow the routes I never finished. The ground first: iron, stone, a forge. Then the sky. Then what lies below, and beyond. Light the old beacon and the sun may remember itself.',
        ]),
    'iron': dict(
        title='Logbook: Iron', author='Courier Mara Venn',
        pages=[
            'Iron remembers the routes. Every gate along the skyway was bolted with it, and every bolt still hums if you hold it close.',
            'Forge what you need. There are things in the dark that do not care for wings.',
        ]),
    'lenses': dict(
        title='Logbook: Lenses', author='Courier Mara Venn',
        pages=[
            'The beacons burned through lenses of diamond. Bring a few along. You will want to see clearly where you are going.',
        ]),
    'the_first_harbor': dict(
        title='Logbook: The First Harbor', author='Courier Mara Venn',
        pages=[
            'The Aether was our first harbor. The clouds are thin but the gates are old, and something still keeps them.',
            'Do not land where the stones are too clean.',
        ]),
    'the_fleet': dict(
        title='Logbook: The Fleet', author='Courier Mara Venn',
        pages=[
            'They tried to cross by sea when the wind failed. Their logs end on the same page, mid-sentence.',
            'I will not finish it for them.',
        ]),
    'the_lowest_gate': dict(
        title='Logbook: The Lowest Gate', author='Courier Mara Venn',
        pages=[
            'The lowest gate is in the Nether, where the old pilots fed the beacons. The heat has not changed. The company has.',
        ]),
    'the_lamps': dict(
        title='Logbook: The Lamps', author='Courier Mara Venn',
        pages=[
            'Their lamps were lit by hand, each night, by a crew of six. The walls are still warm. I did not go in. Perhaps you can.',
        ]),
    'a_warning': dict(
        title='Logbook: A Warning', author='Courier Mara Venn',
        pages=[
            'The last beacon needed a lantern no flame can fill. The old crew called it a Wither Skull. I think it is a warning, not a fuel.',
        ]),
    'the_eyes': dict(
        title='Logbook: The Eyes', author='Courier Mara Venn',
        pages=[
            'Past the gates lies the End, and the eyes point to it like compass needles. I never found out who made them.',
            'I am not sure I want to.',
        ]),
    'the_far_shore': dict(
        title='Logbook: The Far Shore', author='Courier Mara Venn',
        pages=[
            'Dark, and quiet, and the ground is an island. The sun above it is as black as ours.',
            'There is something circling it.',
        ]),
    'the_city': dict(
        title='Logbook: The City', author='Courier Mara Venn',
        pages=[
            'A city of purple stone, empty but for the ships that hang off its sides. Wings of a kind, unclaimed. I left them where they were.',
        ]),
    'the_last_ember': dict(
        title='Logbook: The Last Ember', author='Courier Mara Venn',
        pages=[
            "It was never a dragon guarding the dark. It was the dark's last breath. When it falls, there is a light beneath it.",
            'Take it. Do not look at it too long.',
        ]),
    'the_last_page': dict(
        title='Logbook: The Last Page', author='Courier Mara Venn',
        pages=[
            'You have read my words and gone further than I did. Thank you.',
            'Fly high. The sky has been waiting for a Courier.',
        ]),
}
book.registry.update(BOOKS)


CHAPTERS = [
    Chapter('start_here', 'Start Here', group='Quests', icon='elytra{Damage:0}', order=0, auto='enabled', quests=[
        Q('Welcome Aboard', 'dim overworld', 'elytra{Damage:0,Unbreakable:1b}, 64 rocket, travelersbackpack:standard',
          desc='Your wings are waiting. One unbreakable elytra, a stack of rockets and a backpack to carry your gear.', sub='Free starter kit', at=(0, 0)),
    ]),
    Chapter('elytra_start', 'Taking Flight', group='Quests', icon='elytra{Damage:0}', order=2, quests=[
        Q('Target Practice', 'kill skeleton 3', 'gun:m1911 loaded, 40 ammo:45acp',
          desc='Skeletons are a good first test for your new sidearm. Take out three of them.', at=(0, 0)),
        Q('First Flight', 'fly 1km', '32 rocket',
          desc='Glide a total of one kilometre with an elytra.', at=(2, 0), after='Target Practice'),
        Q('Night Sky Hunter', 'kill phantom 5', '48 rocket',
          desc='Phantoms own the sky at night. Shoot down five of them.', at=(4, 0), after='First Flight'),
        Q('Outpost Scout', 'structure pillager_outpost', '64 rocket',
          desc='Pillager outposts are easy to spot from the air. Find one, but stay out of crossbow range.', at=(6, 0), after='Night Sky Hunter'),
        Q('Scenic Route', 'fly 5km', '64 rocket',
          desc='Fly five kilometres in total. No rush, just enjoy the view.', sub='Optional', at=(0, 2), after='First Flight', optional=True),
        Q('Long Haul', 'fly 10km', '96 rocket, 64 ammo:45acp',
          desc='Ten kilometres in the air. Bring spare rockets and something to repair your wings.', sub='Optional', at=(2, 2), optional=True),
        Q('Nether Glider', 'dim the_nether', '64 rocket',
          desc='Take a trip through a Nether portal.', sub='Optional', at=(4, 2), after='Target Practice', optional=True),
        Q('Into the End', 'dim the_end', '64 rocket',
          desc='Find the stronghold and step through the End portal.', sub='Optional', at=(6, 2), after='Night Sky Hunter', optional=True),
        Q("Sky's the Limit", 'adv end/elytra', ['64 rocket', named('netherite_chestplate{Damage:0,Unbreakable:1b}', "Skyfarer's Plate"), '100 ammo:9mm'],
          desc=['Find an elytra in an End city ship.', 'Reward: an unbreakable netherite chestplate to wear under your wings.'], sub='Optional', at=(8, 2), after='Into the End', optional=True),
        Q('Ghast Hunter', 'kill ghast 1', '64 rocket, gun:ak47, 150 ammo:762x39',
          desc='Ghasts float, and so do you. Take one down.', sub='Hard', at=(0, 4)),
        Q('Deep Dark Delve', 'structure ancient_city', '64 rocket, gun:m700, 40 ammo:30_06',
          desc='Something is sleeping beneath the ground. Find an Ancient City, and be quiet about it.', sub='Hard', at=(2, 4), after='Night Sky Hunter'),
        Q("Elder's Wrath", 'kill elder_guardian 1', '64 rocket, 4 golden_apple, 8 diamond',
          desc='Raid an ocean monument and defeat its elder guardian.', sub='Hard', at=(4, 4), after='Night Sky Hunter'),
        Q('Wither Sky', 'kill wither 1', '128 rocket, 2 netherite_ingot',
          desc='Summon the Wither and survive. Flying helps.', sub='Hard', at=(6, 4), after='Ghast Hunter'),
        Q('End City Raid', 'structure end_city', '64 rocket, 4 shulker_shell',
          desc="Land on an End city and claim what's inside.", sub='Hard', at=(8, 4), after='Into the End'),
        Q('Dragon Slayer', 'kill ender_dragon 1', '192 rocket, gun:m4a1, 4 netherite_ingot, 192 ammo:556x45',
          desc='The big one. Defeat the Ender Dragon.', sub='Hard', at=(10, 4), after='End City Raid'),
    ]),
    # "Zwischen den Zeiten": the story, splitting into an ancient path and a modern (TaCZ) path.
    # Quests stay invisible until their predecessor is complete (chapter setting below).
    Chapter('story_ashen_skyways', 'Zwischen den Zeiten', group='Quests', icon='written_book', order=1,
            extra={'hide_quest_until_deps_complete': True}, quests=[
        Q('Eisern aber weich', 'adv story/smelt_iron', 'aether:golden_oak_sapling',
          desc='In alten Zeiten kämpfte man unerbittlich mit Stahl gegen die Dunkelheit des Nethers, doch nur der goldene Aether hielt die Ungeheuer der Nacht fern.',
          at=(0, 0), icon='iron_ingot'),
        Q('Kupferpfeil', 'have copper_ingot', '1 ammo:9mm',
          desc='Fun Fact: Kupfer ist tatsächlich antibakteriell, ob das auch für die fliegenden Kugeln gilt?',
          at=(1.5, 0), icon='copper_ingot'),
        Q('Schwerter und Kugeln', 'adv elytra_extras:kackhaufen',
          [command('/execute as @p at @s run function elytra_extras:messenger/arrive')],  # hidden: Der Bote appears
          sub='Was passiert, wenn ich beides kombiniere?',
          desc='Das war ein Griff ins Klo - und wer ist dieser komische Vogel?',
          at=(0.75, 1.5), after=['Eisern aber weich', 'Kupferpfeil'], icon=KACKHAUFEN,
          extra={'hide_text_until_complete': True}),
    ]),
    Chapter('good_deeds', 'Good Deeds', group='Quests', icon='shulker_box', order=3, sub='Good deed', quests=[
        Q('Hero of the Village', 'adv adventure/hero_of_the_village', [named('red_shulker_box', "Hero's Box")],
          desc=['Defend a village from a raid and earn its thanks.', 'Reward: a red shulker box.'], at=(0, 0)),
        Q('Zombie Doctor', 'adv story/cure_zombie_villager', [named('green_shulker_box', "Doctor's Box")],
          desc=['Cure a zombie villager and give them their life back.', 'Reward: a green shulker box.'], at=(1.5, 0)),
        Q('Hired Help', 'adv adventure/summon_iron_golem', [named('light_gray_shulker_box', "Guardian's Box")],
          desc=['Build an iron golem to guard a village.', 'Reward: a light gray shulker box.'], at=(3, 0)),
        Q('Best Friends Forever', 'adv husbandry/tame_an_animal', [named('brown_shulker_box', "Companion's Box")],
          desc=['Tame an animal and give it a home.', 'Reward: a brown shulker box.'], at=(4.5, 0)),
        Q('Making a Family', 'adv husbandry/breed_an_animal', [named('pink_shulker_box', "Keeper's Box")],
          desc=['Breed two animals.', 'Reward: a pink shulker box.'], at=(0, 1.5)),
        Q('A Seedy Place', 'adv husbandry/plant_seed', [named('lime_shulker_box', "Gardener's Box")],
          desc=['Plant a seed and watch it grow.', 'Reward: a lime shulker box.'], at=(1.5, 1.5)),
        Q('Bee Our Guest', 'adv husbandry/safely_harvest_honey', [named('yellow_shulker_box', "Beekeeper's Box")],
          desc=['Collect honey from a hive without angering the bees.', 'Reward: a yellow shulker box.'], at=(3, 1.5)),
        Q('Total Beelocation', 'adv husbandry/silk_touch_nest', [named('orange_shulker_box', "Nest Mover's Box")],
          desc=['Move a bee nest, bees and all, with Silk Touch.', 'Reward: an orange shulker box.'], at=(4.5, 1.5)),
        Q('Fishy Business', 'adv husbandry/fishy_business', [named('cyan_shulker_box', "Angler's Box")],
          desc=['Catch a fish to feed someone.', 'Reward: a cyan shulker box.'], at=(0, 3)),
        Q('A Fair Deal', 'adv adventure/trade', [named('blue_shulker_box', "Trader's Box")],
          desc=['Trade with a villager.', 'Reward: a blue shulker box.'], at=(1.5, 3)),
        Q('A Complete Catalogue', 'adv husbandry/complete_catalogue', [named('white_shulker_box', "Cat Keeper's Box")],
          desc=['Tame every kind of cat.', 'Reward: a white shulker box.'], at=(3, 3)),
        Q('Two by Two', 'adv husbandry/bred_all_animals', [named('light_blue_shulker_box', "Ark Builder's Box")],
          desc=['Breed every kind of animal.', 'Reward: a light blue shulker box.'], at=(4.5, 3)),
        Q('Sweet Dreams', 'adv adventure/sleep_in_bed', [named('purple_shulker_box', "Dreamer's Box")],
          desc=['Sleep in a bed and let the night pass.', 'Reward: a purple shulker box.'], at=(0, 4.5)),
        Q('Bring Home the Beacon', 'adv nether/create_beacon', [named('black_shulker_box', "Lightkeeper's Box")],
          desc=['Build a beacon and light up the land.', 'Reward: a black shulker box.'], at=(1.5, 4.5)),
        Q('Surge Protector', 'adv adventure/lightning_rod_with_villager_no_fire', [named('gray_shulker_box', "Protector's Box")],
          desc=['Protect a villager from lightning with a rod.', 'Reward: a gray shulker box.'], at=(3, 4.5)),
        Q('A Balanced Diet', 'adv husbandry/balanced_diet', [named('magenta_shulker_box', "Cook's Box")],
          desc=['Eat everything edible, and stay healthy.', 'Reward: a magenta shulker box.'], at=(4.5, 4.5)),
        Q('Pillar of the Community', 'check', [named('shulker_box', 'Pillar of the Community'), '16 emerald', 'totem_of_undying'],
          desc=['Every deed done. The whole community knows your name.', 'Check this off to claim the last box.'], sub='Good deed, finale', at=(2.25, 6.5), after=['Zombie Doctor', 'Hired Help', 'Best Friends Forever', 'A Seedy Place', 'Bee Our Guest', 'Fishy Business', 'A Fair Deal', 'Two by Two', 'Sweet Dreams']),
    ]),
    Chapter('long_term', 'Long-Term Goals', group='Quests', icon='clock', order=4, quests=[
        Q('Frequent Flyer', 'fly 25km', '10 diamond',
          desc='Glide 25 km in total with your elytra.', sub='Sky miles', at=(0, 0)),
        Q('Cross-Country', 'fly 50km', '16 emerald',
          desc='Glide 50 km in total.', sub='Sky miles', at=(1.5, 0), after='Frequent Flyer'),
        Q('Skyward Bound', 'fly 100km', 'netherite_ingot, 24 emerald',
          desc='Glide 100 km in total.', sub='Sky miles', at=(3, 0), after='Cross-Country'),
        Q('Sky Legend', 'fly 250km', 'gun:minigun, 192 ammo:308, 4 netherite_ingot',
          desc='Glide 250 km in total. Few ever get this far.', sub='Sky miles, capstone', at=(4.5, 0)),
        Q('Hunter I', 'stat mob_kills 250', '16 gold_ingot, 64 ammo:9mm',
          desc='Defeat 250 mobs in total.', sub='Mob kills', at=(0, 2)),
        Q('Hunter II', 'stat mob_kills 1000', '10 diamond, 120 ammo:556x45',
          desc='Defeat 1,000 mobs in total.', sub='Mob kills', at=(1.5, 2)),
        Q('Hunter III', 'stat mob_kills 2500', '16 emerald, gun:hk416d, 150 ammo:556x45',
          desc='Defeat 2,500 mobs in total.', sub='Mob kills', at=(3, 2)),
        Q('Hunter IV', 'stat mob_kills 5000', 'gun:deagle_golden, 96 ammo:357mag, 2 netherite_ingot',
          desc='Defeat 5,000 mobs in total.', sub='Mob kills, capstone', at=(4.5, 2)),
        Q('Deep Warden', 'kill warden 1', '2 netherite_ingot, 16 emerald, att:ammo_mod_he',
          desc='Defeat a Warden. Move quietly, and have an escape plan.', sub='Boss', at=(0, 4)),
        Q('Sun Spirit', 'kill aether:sun_spirit 1', '12 diamond, att:ammo_mod_i',
          desc='Defeat the Sun Spirit in the Aether.', sub='Boss', at=(1.5, 4)),
        Q('Valkyrie Queen', 'kill aether:valkyrie_queen 1', '12 diamond, att:ammo_mod_hp',
          desc='Defeat the Valkyrie Queen in the Aether.', sub='Boss', at=(3, 4)),
        Q('Monster Hunter', 'adv adventure/kill_all_mobs', '24 emerald, totem_of_undying, 2 enchanted_golden_apple',
          desc='Earn the vanilla Monsters Hunted advancement by defeating every hostile mob.', sub='Achievement', at=(4.5, 4)),
        Q('World Traveler', 'adv adventure/adventuring_time', '24 emerald, 4 diamond',
          desc='Earn the vanilla Adventuring Time advancement by visiting every biome.', sub='Exploration', at=(0, 6)),
        Q('Mansion Raider', 'structure mansion', '8 diamond, totem_of_undying',
          desc='Find a woodland mansion.', sub='Exploration', at=(1.5, 6)),
        Q('Bastion Breaker', 'structure bastion_remnant', '8 diamond, 16 gold_ingot',
          desc='Find a bastion remnant in the Nether.', sub='Exploration', at=(3, 6)),
        Q('Settled In', 'playtime 10h', '16 gold_ingot',
          desc='Play for 10 hours.', sub='Play time', at=(0, 8)),
        Q('Veteran', 'playtime 25h', '10 diamond',
          desc='Play for 25 hours.', sub='Play time', at=(1.5, 8), after='Settled In'),
        Q('Lifer', 'playtime 50h', '16 emerald',
          desc='Play for 50 hours.', sub='Play time', at=(3, 8), after='Veteran'),
        Q('Sky Dweller', 'playtime 100h', '32 emerald, netherite_ingot',
          desc='Play for 100 hours.', sub='Play time, capstone', at=(4.5, 8), after='Lifer'),
    ]),
    Chapter('backpack_upgrades', 'Backpack Upgrades', group='Quests', icon='travelersbackpack:standard', order=5, auto='no_toast', quests=[
        Q('Sticky Fingers', 'kill zombie 25', 'travelersbackpack:pickup_upgrade',
          desc='Clear out 25 zombies and your bag learns to grab loot by itself.', sub='Pickup Upgrade', at=(0, 0), icon='travelersbackpack:pickup_upgrade'),
        Q('Portable Workbench', 'kill skeleton 20', 'travelersbackpack:crafting_upgrade',
          desc='Put 20 skeletons down. A crafting grid for the road is your reward.', sub='Crafting Upgrade', at=(2, 0), icon='travelersbackpack:crafting_upgrade'),
        Q('Never Hungry', 'give 32 cooked_beef', 'travelersbackpack:feeding_upgrade',
          desc='Hand over 32 cooked beef and the bag will feed you on its own.', sub='Feeding Upgrade', at=(4, 0), icon='travelersbackpack:feeding_upgrade'),
        Q('Liquid Cargo', 'adv husbandry/tactical_fishing', 'travelersbackpack:tanks_upgrade',
          desc='Catch a fish in a bucket. Two fluid tanks for your pack.', sub='Tanks Upgrade', at=(6, 0), after='Never Hungry', icon='travelersbackpack:tanks_upgrade'),
        Q('Hot Pocket', 'dim the_nether', 'travelersbackpack:furnace_upgrade',
          desc='Step into the Nether and carry your own furnace home.', sub='Furnace Upgrade', at=(0, 2), icon='travelersbackpack:furnace_upgrade'),
        Q('Smokehouse', 'give 24 cooked_porkchop', 'travelersbackpack:smoker_upgrade',
          desc='Feed the smoker 24 cooked porkchops to prove you know the craft.', sub='Smoker Upgrade', at=(2, 2), icon='travelersbackpack:smoker_upgrade'),
        Q('Forge on Your Back', 'kill blaze 15', 'travelersbackpack:blast_furnace_upgrade',
          desc='Burn down 15 blazes. Your reward smelts ores in a flash.', sub='Blast Furnace Upgrade', at=(4, 2), icon='travelersbackpack:blast_furnace_upgrade'),
        Q('Soundtrack of the Skies', 'adv adventure/play_jukebox_in_meadows', 'travelersbackpack:jukebox_upgrade',
          desc='Play a music disc in a meadow, then take the music with you.', sub='Jukebox Upgrade', at=(6, 2), icon='travelersbackpack:jukebox_upgrade'),
        Q('Gravity Well', 'kill phantom 10', 'travelersbackpack:magnet_upgrade',
          desc='Take down 10 phantoms. Loot will fly to you afterwards.', sub='Magnet Upgrade', at=(0, 4), icon='travelersbackpack:magnet_upgrade'),
        Q('Black Hole', 'kill enderman 10', 'travelersbackpack:void_upgrade',
          desc='Banish 10 endermen. Junk goes into the void for good.', sub='Void Upgrade', at=(2, 4), after='Gravity Well', icon='travelersbackpack:void_upgrade'),
        Q('Always Stocked', 'dim the_end', 'travelersbackpack:refill_upgrade',
          desc='Reach the End and your hotbar will never run dry again.', sub='Refill Upgrade', at=(4, 4), after='Black Hole', icon='travelersbackpack:refill_upgrade'),
    ]),
    # Boss dungeons from the elytra_dungeons datapack (questtools/dungeongen.py). Each quest: find the
    # structure, then defeat its boss (the datapack grants the advancement to everyone within 48-64 blocks).
    Chapter('boss_dungeons', 'Boss Dungeons', group='Quests', icon='wither_skeleton_skull', order=6, reward_line=True, quests=[
        Q('Ash to Ash', 'structure elytra_dungeons:ashen_barrow; adv elytra_dungeons:bosses/ashen_warlord',
          'gun:scar_l, 120 ammo:556x45',
          desc=['A ring of black stone in the badlands hides a shaft into the dark. Something on a throne is waiting below.',
                'Find an Ashen Barrow and defeat the Ashen Warlord.'],
          at=(0, 0), icon='wither_skeleton_skull'),
        Q('Eye of the Storm', 'structure elytra_dungeons:storm_spire; adv elytra_dungeons:bosses/tempest_herald',
          'gun:m107, 30 ammo:50bmg',
          desc=['High above the clouds a stone crown floats on the wind. Only wings can reach it.',
                'Find a Storm Spire and destroy the Tempest Herald. Aim for the ruby on its forehead.'],
          at=(2, 0), icon='ghast_tear'),
        Q('Into the Hollow', 'structure elytra_dungeons:rift_gate; adv elytra_dungeons:bosses/hollow_magus',
          'gun:fn_evolys, 96 ammo:308',
          desc=['Crying obsidian frames stand where the world is thin. Step through one.',
                'Break the Hollow Magus\'s crystal shield and defeat him.'],
          at=(4, 0), icon='end_crystal'),
    ]),
    # Horde leaders from the elytra_hordes datapack (questtools/leadergen.py); advancements modpack:leaders/*
    Chapter('horde_leaders', 'Horde Leaders', group='Quests', icon='zombie_head', order=7, sub='Horde leader', quests=[
        Q('Cut Off the Head', 'adv modpack:leaders/kill_any', '36 ammo:12g, 60 ammo:556x45',
          desc=['Every horde follows one leader. Kill it and the rest lose their nerve.', 'Kill any horde leader.'],
          sub='Any leader', at=(3, 0), icon='zombie_head'),
        Q('Läufer', 'adv modpack:leaders/kill_laeufer', 'att:muzzle_choke_sg, 36 ammo:12g',
          desc=['Fast and fragile. It sprints the moment it sees you.', 'Counter: a shotgun at close range.'],
          at=(0, 2), icon='sugar'),
        Q('Brecher', 'adv modpack:leaders/kill_brecher', 'att:ammo_mod_fmj, 30 ammo:338',
          desc=['Wrapped in iron and almost impossible to knock back. Body shots barely scratch it.',
                'Counter: guns with high armour piercing (AI AWP, M95), FMJ ammo, headshots.'],
          at=(1.5, 2), icon='iron_chestplate'),
        Q('Spucker', 'adv modpack:leaders/kill_spucker', 'att:scope_standard_8x, 36 ammo:30_06',
          desc=['Keeps its distance and spits poison to drive you out of cover.', 'Counter: a sniper rifle.'],
          at=(3, 2), icon='spider_eye'),
        Q('Schreier', 'adv modpack:leaders/kill_schreier', 'att:muzzle_silencer_ptilopsis, 60 ammo:9mm',
          desc=['Its scream calls more of the dead. Loud gunfire makes it scream sooner.',
                'Counter: a suppressor, and kill it first.'],
          at=(4.5, 2), icon='goat_horn'),
        Q('Kriecher', 'adv modpack:leaders/kill_kriecher', 'att:laser_peq6, 16 torch',
          desc=['Low to the ground and invisible in the dark. If it grabs your legs, you will not get away quickly.',
                'Counter: light the area up, then finish it in melee.'],
          at=(6, 2), icon='torch'),
        Q('Platzer', 'adv modpack:leaders/kill_platzer', '6 ammo:40mm, 8 gunpowder',
          desc=['Swollen and ready to burst. When it dies, everything nearby gets hurt, zombies included.',
                'Counter: keep your distance.'],
          at=(7.5, 2), icon='tnt'),
        Q('Leader Hunter',
          'adv modpack:leaders/kill_laeufer; adv modpack:leaders/kill_brecher; adv modpack:leaders/kill_spucker; '
          'adv modpack:leaders/kill_schreier; adv modpack:leaders/kill_kriecher; adv modpack:leaders/kill_platzer',
          'att:ammo_mod_he, 30 ammo:50bmg',
          desc=['Kill one leader of every type.'], sub='All six', at=(3.75, 4), icon='zombie_head'),
    ]),
    Chapter('overworld', 'Overworld Bounties', group='Dimensions', icon='grass_block', order=0, reward_line=True, quests=[
        Q('Zombie Stopper', 'kill zombie 10', 'gun:glock_17, 60 ammo:9mm, 16 rocket',
          desc='Ten zombies. A simple pistol should do.', at=(0, 0)),
        Q('Web Cutter', 'kill spider 10', 'gun:db_short, 24 ammo:12g, 16 rocket',
          desc='Spiders are fast and nasty up close. A shotgun helps.', at=(2, -1), after='Zombie Stopper'),
        Q('Creeper Crowd', 'kill creeper 8', 'gun:uzi, 90 ammo:9mm, 16 rocket',
          desc='Shoot them before they get close.', at=(2, 1), after='Zombie Stopper'),
        Q('Raid Breaker', 'kill pillager 10', 'gun:hk_mp5a5, 90 ammo:9mm, 16 rocket',
          desc='Take out pillagers from range.', at=(4, 0), after=['Web Cutter', 'Creeper Crowd']),
        Q('Beast Slayer', 'kill ravager 1', 'gun:sks_tactical, 60 ammo:762x39, 16 rocket',
          desc='A ravager is tough. Bring your best shots.', at=(6, 0)),
    ]),
    Chapter('nether', 'Nether Bounties', group='Dimensions', icon='netherrack', order=1, reward_line=True, quests=[
        Q('Through the Portal', 'dim the_nether', '32 rocket',
          desc='Enter the Nether.', sub='Start here', at=(0, 0)),
        Q('Blaze Runner', 'kill blaze 10', 'gun:ak47, 120 ammo:762x39, 16 rocket',
          desc='Blazes are best fought in the fortresses.', at=(2, -1)),
        Q('Bone Crusher', 'kill wither_skeleton 6', 'gun:aa12, 48 ammo:12g, 16 rocket',
          desc='Wither skeletons patrol the fortresses.', at=(2, 1)),
        Q('Hoglin Hunt', 'kill hoglin 8', 'gun:m249, 150 ammo:556x45, 16 rocket',
          desc='Hoglins charge. Keep moving.', at=(4, -1), after='Blaze Runner'),
        Q('Brute Force', 'kill piglin_brute 3', 'gun:m700, 40 ammo:30_06, 16 rocket',
          desc='Brutes guard the bastions. Expect a fight.', at=(4, 1), after='Bone Crusher'),
    ]),
    Chapter('aether', 'Aether Hunts', group='Dimensions', icon='aether:aether_portal_frame', order=2, reward_line=True, quests=[
        Q('Sky Kingdom', 'dim aether:the_aether', '32 rocket',
          desc='Enter the Aether.', sub='Start here', at=(0, 0)),
        Q('Zephyr Chase', 'kill aether:zephyr 5', 'gun:vector45, 90 ammo:45acp, 16 rocket',
          desc='Zephyrs fly and spit snowballs. Good target practice.', at=(2, -1)),
        Q('Stone Cold', 'kill aether:cockatrice 5', 'gun:m870, 32 ammo:12g, 16 rocket',
          desc='Cockatrices hit hard. Keep your distance.', at=(2, 1)),
        Q('Sentry Shutdown', 'kill aether:sentry 8', 'gun:m4a1, 120 ammo:556x45, 16 rocket',
          desc='Sentries guard the dungeons.', at=(4, -1)),
        Q('Gatekeeper', 'kill aether:slider 1', 'gun:spr15hb, 60 ammo:556x45, 16 rocket',
          desc="Defeat the Slider, the Aether's dungeon boss.", at=(4, 1), after='Sentry Shutdown'),
    ]),
    Chapter('the_end', 'End Trophies', group='Dimensions', icon='end_stone', order=3, reward_line=True, quests=[
        Q('The Final Frontier', 'dim the_end', '64 rocket',
          desc='Enter the End.', sub='Start here', at=(0, 0)),
        Q('Enderman Ambush', 'kill enderman 10', 'gun:scar_h, 60 ammo:308, 32 rocket',
          desc="Don't look them in the eye.", at=(2, -1)),
        Q('Shell Game', 'kill shulker 4', 'gun:aug, 120 ammo:556x45, 32 rocket',
          desc='Shulkers hide in End cities.', at=(2, 1)),
        Q('End City Raid', 'structure end_city', 'gun:ai_awp, 30 ammo:338, 48 rocket',
          desc='Land on an End city.', at=(4, -1), after='Enderman Ambush'),
        Q("Dragon's End", 'kill ender_dragon 1', 'gun:m95, 30 ammo:50bmg, 64 rocket',
          desc='The best weapon in the pack, for the hardest fight.', at=(6, 0), after='Shell Game'),
    ]),
    Chapter('gun_shop', 'Gun Shop', group='Shop', icon='emerald', order=0, repeat=True, auto='no_toast', layout=Grid(cols=9), quests=[
        # gun id                  name                        price             tier
        gun('springfield1873',       'Springfield 1873',         '6 gold_ingot',   'Gold tier'),
        gun('db_short',              'Sawed-off Double Barrel',  '7 gold_ingot',   'Gold tier'),
        gun('glock_17',              'Glock 17',                 '10 gold_ingot',  'Gold tier'),
        gun('m9a4',                  'M9A4',                     '10 gold_ingot',  'Gold tier'),
        gun('cz75',                  'CZ 75',                    '10 gold_ingot',  'Gold tier'),
        gun('m1911',                 'M1911',                    '11 gold_ingot',  'Gold tier'),
        gun('db_long',               'Double Barrel (Long)',     '11 gold_ingot',  'Gold tier'),
        gun('b93r',                  'B93R',                     '15 gold_ingot',  'Gold tier'),
        gun('m870',                  'M870',                     '19 gold_ingot',  'Gold tier'),
        gun('uzi',                   'Uzi',                      '19 gold_ingot',  'Gold tier'),
        gun('type_81',               'Type 81',                  '20 gold_ingot',  'Gold tier'),
        gun('hk_mp5a5',              'HK MP5A5',                 '24 gold_ingot',  'Gold tier'),
        gun('m16a1',                 'M16A1',                    '7 diamond',      'Diamond tier'),
        gun('p320',                  'P320',                     '8 diamond',      'Diamond tier'),
        gun('m16a4',                 'M16A4',                    '8 diamond',      'Diamond tier'),
        gun('m4a1',                  'M4A1',                     '8 diamond',      'Diamond tier'),
        gun('ak47',                  'AK-47',                    '8 diamond',      'Diamond tier'),
        gun('aug',                   'AUG',                      '9 diamond',      'Diamond tier'),
        gun('hk_mk23',               'HK Mk23',                  '9 diamond',      'Diamond tier'),
        gun('sks_tactical',          'SKS Tactical',             '9 diamond',      'Diamond tier'),
        gun('rhino357',              'Rhino .357',               '10 diamond',     'Diamond tier'),
        gun('qbz_95',                'QBZ-95',                   '10 diamond',     'Diamond tier'),
        gun('m700',                  'M700',                     '12 diamond',     'Diamond tier'),
        gun('kar98',                 'Kar98k',                   '13 diamond',     'Diamond tier'),
        gun('lonetrail',             'Lonetrail',                '13 diamond',     'Diamond tier'),
        gun('scar_l',                'SCAR-L',                   '14 diamond',     'Diamond tier'),
        gun('timeless50',            'Timeless .50',             '14 diamond',     'Diamond tier'),
        gun('ump45',                 'UMP45',                    '16 diamond',     'Diamond tier'),
        gun('deagle',                'Desert Eagle',             '16 diamond',     'Diamond tier'),
        gun('rpg7',                  'RPG-7',                    '18 diamond',     'Diamond tier'),
        gun('m320',                  'M320 Grenade Launcher',    '19 diamond',     'Diamond tier'),
        gun('rpk',                   'RPK',                      '21 diamond',     'Diamond tier'),
        gun('hk_g3',                 'HK G3',                    '21 diamond',     'Diamond tier'),
        gun('m1014',                 'M1014',                    '22 diamond',     'Diamond tier'),
        gun('fn_fal',                'FN FAL',                   '23 diamond',     'Diamond tier'),
        gun('p90',                   'P90',                      '23 diamond',     'Diamond tier'),
        gun('qbz_191',               'QBZ-191',                  '24 diamond',     'Diamond tier'),
        gun('spr15hb',               'SPR-15HB',                 '26 diamond',     'Diamond tier'),
        gun('g36k',                  'G36K',                     '27 diamond',     'Diamond tier'),
        gun('hk416d',                'HK416D',                   '27 diamond',     'Diamond tier'),
        gun('deagle_golden',         'Golden Desert Eagle',      '27 diamond',     'Diamond tier'),
        gun('aa12',                  'AA-12',                    '19 emerald',     'Emerald tier, rare'),
        gun('scar_h',                'SCAR-H',                   '21 emerald',     'Emerald tier, rare'),
        gun('spas_12',               'SPAS-12',                  '22 emerald',     'Emerald tier, rare'),
        gun('mk14',                  'Mk14 EBR',                 '22 emerald',     'Emerald tier, rare'),
        gun('m249',                  'M249',                     '23 emerald',     'Emerald tier, rare'),
        gun('vector45',              'Vector 45',                '24 emerald',     'Emerald tier, rare'),
        gun('fn_evolys',             'FN Evolys',                '37 emerald',     'Emerald tier, rare'),
        gun('taurus500',             'Taurus 500',               '46 emerald',     'Emerald tier, rare'),
        gun('ai_awp',                'AI AWP',                   '55 emerald',     'Emerald tier, rare'),
        gun('m95',                   'M95',                      '64 emerald',     'Emerald tier, rare'),
        gun('m107',                  'M107',                     '64 emerald',     'Emerald tier, rare'),
        gun('minigun',               'Minigun',                  '64 emerald',     'Emerald tier, rare'),
    ]),
    Chapter('rockets', 'Rockets', group='Shop', icon='rocket', order=1, repeat=True, auto='no_toast', layout=Pairs(cols=3), quests=[
        rockets('gunpowder',     8),
        rockets('rotten_flesh',  1),
        rockets('bone',          4),
    ]),
    Chapter('ammo_pistols_smgs', 'Ammo: Pistols and SMGs', group='Shop', icon='ammo:9mm', order=2, repeat=True, auto='no_toast', layout=Pairs(cols=5), quests=[
        # AMMO PRICING: "per" = rounds for one single trade. The bulk trade is always one full stack
        # of that calibre (TaCZ stack sizes differ: 60, 48, 42, 36, 30, 6), so per must divide the stack.
        # Handguns and slow-firing guns pay less per round; fast automatics and big calibres pay more.
        # ammo id          name               price per single trade      rounds   one stack costs
        ammo('9mm',           '9mm',             '1 copper_ingot',            per=5),  # 60 = 12 copper
        ammo('45acp',         '.45 ACP',         '1 copper_ingot',            per=5),  # 60 = 12 copper
        ammo('22wmr',         '.22 WMR',         '1 copper_ingot',            per=8),  # 64 = 8 copper, one slow revolver
        ammo('46x30',         '4.6x30',          '1 copper_ingot',            per=5),  # 60 = 12 copper
        ammo('57x28',         '5.7x28',          '1 copper_ingot',            per=5),  # 60 = 12 copper
        ammo('762x25',        '7.62x25',         '1 copper_ingot',            per=5),  # 60 = 12 copper
        ammo('357mag',        '.357 Magnum',     '1 copper_ingot',            per=4),  # 48 = 12 copper, revolvers
        ammo('50ae',          '.50 AE',          '1 copper_ingot',            per=3),  # 48 = 16 copper
        ammo('500mag',        '.500 Magnum',     '1 copper_ingot',            per=2),  # 42 = 21 copper, 5-shot hand cannon
    ]),
    Chapter('ammo_rifles', 'Ammo: Rifles', group='Shop', icon='ammo:556x45', order=3, repeat=True, auto='no_toast', layout=Pairs(cols=5), quests=[
        # ammo id          name               price per single trade      rounds   one stack costs
        ammo('556x45',        '5.56x45',         '1 iron_ingot',              per=4),  # 60 = 15 iron
        ammo('762x39',        '7.62x39',         '1 iron_ingot',              per=3),  # 60 = 20 iron, hits harder than 5.56
        ammo('545x39',        '5.45x39',         '1 iron_ingot',              per=4),  # 60 = 15 iron
        ammo('58x42',         '5.8x42',          '1 iron_ingot',              per=4),  # 60 = 15 iron
        ammo('308',           '.308',            '1 iron_ingot',              per=3),  # 48 = 16 iron, battle rifles and MGs
        ammo('68x51fury',     '6.8x51 FURY',     '1 iron_ingot',              per=3),  # 60 = 20 iron
        ammo('762x54',        '7.62x54R',        '1 iron_ingot',              per=3),  # 60 = 20 iron
        ammo('792x57',        '7.92x57',         '1 iron_ingot',              per=3),  # 36 = 12 iron, bolt-action Kar98k
    ]),
    Chapter('ammo_heavy', 'Ammo: Snipers and Heavy', group='Shop', icon='ammo:50bmg', order=4, repeat=True, auto='no_toast', layout=Pairs(cols=5), quests=[
        # ammo id          name               price per single trade      rounds   one stack costs
        ammo('30_06',         '.30-06',          '1 iron_ingot',              per=3),  # 36 = 12 iron, bolt-action / single shot
        ammo('338',           '.338 Lapua',      '1 iron_ingot',              per=2),  # 30 = 15 iron
        ammo('45_70',         '.45-70',          '1 iron_ingot',              per=3),  # 48 = 16 iron, single shot
        ammo('50bmg',         '.50 BMG',         '1 iron_ingot',              per=1),  # 30 = 30 iron, the strongest round
    ]),
    Chapter('ammo_shotguns_launchers', 'Ammo: Shotguns and Launchers', group='Shop', icon='ammo:rpg_rocket', order=5, repeat=True, auto='no_toast', layout=Pairs(cols=5), quests=[
        # ammo id          name               price per single trade      rounds   one stack costs
        ammo('12g',           '12 Gauge',        '1 iron_ingot',              per=3),  # 36 = 12 iron
        ammo('40mm',          '40mm Grenade',    '2 gunpowder + 2 iron_ingot', per=1), # 6 = 12 gunpowder + 12 iron
        ammo('rpg_rocket',    'RPG Rocket',      '3 gunpowder + 3 iron_ingot', per=1), # 6 = 18 gunpowder + 18 iron
    ]),
    Chapter('att_sights', 'Attachments: Sights', group='Attachments', icon='att:sight_deltapoint_pistol', order=0, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Sight', note=ATT_NOTE, quests=[
        att('sight_552',                   '552 Sight',                 '12 iron_ingot + 5 gold_ingot + 6 redstone + 4 glass'),
        att('sight_acro_pistol',           'Acro Pistol Sight',         '4 iron_ingot + 1 redstone'),
        att('sight_acro_rifle',            'Acro Rifle Sight',          '6 iron_ingot + 1 redstone'),
        att('sight_coyote',                'Coyote Sight',              '8 iron_ingot + 4 redstone + 2 glass'),
        att('sight_deltapoint_pistol',     'Deltapoint Pistol Sight',   '4 iron_ingot + 1 redstone'),
        att('sight_deltapoint_rifle',      'Deltapoint Rifle Sight',    '6 iron_ingot + 1 redstone'),
        att('sight_exp3',                  'EXP3 Sight',                '14 iron_ingot + 5 gold_ingot + 8 redstone + 4 glass'),
        att('sight_fastfire_pistol',       'Fastfire Pistol Sight',     '4 iron_ingot + 1 redstone'),
        att('sight_fastfire_rifle',        'Fastfire Rifle Sight',      '6 iron_ingot + 1 redstone'),
        att('sight_okp7',                  'OKP7 Sight',                '4 iron_ingot + 4 redstone + 2 glass'),
        att('sight_pk06_pistol',           'PK06 Pistol Sight',         '4 iron_ingot + 1 redstone'),
        att('sight_pk06_rifle',            'PK06 Rifle Sight',          '6 iron_ingot + 1 redstone'),
        att('sight_rmr_dot',               'RMR Dot Sight',             '4 iron_ingot + 1 redstone'),
        att('sight_sro_dot',               'SRO Dot Sight',             '4 iron_ingot + 1 redstone'),
        att('sight_srs_02',                'SRS 02 Sight',              '6 iron_ingot + 2 redstone + 2 glass'),
        att('sight_t1',                    'T1 Sight',                  '4 iron_ingot + 1 redstone + 1 glass'),
        att('sight_t2',                    'T2 Sight',                  '6 iron_ingot + 1 redstone + 1 glass'),
        att('sight_uh1',                   'UH1 Sight',                 '15 iron_ingot + 6 gold_ingot + 8 redstone + 4 glass'),
    ]),
    Chapter('att_scopes', 'Attachments: Scopes', group='Attachments', icon='att:scope_contender', order=1, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Scope', note=ATT_NOTE, quests=[
        att('scope_1873_6x',               '1873 6X Scope',             '16 copper_ingot + 4 iron_ingot + 4 glass'),
        att('scope_98k',                   '98K Scope',                 '10 iron_ingot + 2 glass'),
        att('scope_acog_ta31',             'ACOG TA31 Scope',           '10 iron_ingot + 6 glass + 8 redstone'),
        att('scope_contender',             'Contender Scope',           '10 iron_ingot + 4 glass'),
        att('scope_elcan_4x',              'Elcan 4X Scope',            '16 iron_ingot + 10 glass + 10 redstone'),
        att('scope_hamr',                  'HAMR Scope',                '18 iron_ingot + 8 glass + 10 redstone'),
        att('scope_lpvo_1_6',              'LPVO 1 6 Scope',            '14 iron_ingot + 8 glass + 8 glowstone_dust + 6 redstone'),
        att('scope_mk5hd',                 'MK5HD Scope',               '24 iron_ingot + 20 glass + 8 glowstone_dust + 8 redstone'),
        att('scope_qmk152',                'QMK152 Scope',              '12 iron_ingot + 16 glass + 10 redstone'),
        att('scope_retro_2x',              'Retro 2X Scope',            '8 iron_ingot + 2 glass'),
        att('scope_standard_8x',           'Standard 8X Scope',         '18 iron_ingot + 16 glass + 8 glowstone_dust + 8 redstone'),
        att('scope_vudu',                  'Vudu Scope',                '14 iron_ingot + 8 glass + 8 glowstone_dust + 6 redstone'),
    ]),
    Chapter('att_muzzles', 'Attachments: Muzzles', group='Attachments', icon='att:muzzle_brake_cthulhu', order=2, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Muzzle', note=ATT_NOTE, quests=[
        att('muzzle_brake_cthulhu',        'Cthulhu Brake',             '16 iron_ingot + 5 gold_ingot'),
        att('muzzle_brake_cyclone_d2',     'Cyclone D2 Brake',          '10 iron_ingot + 4 gold_ingot'),
        att('muzzle_brake_mastiff_sg',     'Mastiff SG Brake',          '18 iron_ingot + 4 gold_ingot'),
        att('muzzle_brake_pioneer',        'Pioneer Brake',             '14 iron_ingot + 5 gold_ingot'),
        att('muzzle_brake_timeless50',     'TIMELESS50 Brake',          '15 iron_ingot + 5 redstone'),
        att('muzzle_brake_trex',           'Trex Brake',                '18 iron_ingot + 6 gold_ingot'),
        att('muzzle_choke_sg',             'SG Choke',                  '20 iron_ingot + 6 gold_ingot'),
        att('muzzle_compensator_trident',  'Trident Compensator',       '10 iron_ingot + 4 gold_ingot'),
        att('muzzle_silencer_knight_qd',   'Knight QD Silencer',        '16 iron_ingot + 6 leather + 2 redstone'),
        att('muzzle_silencer_mirage',      'Mirage Silencer',           '10 iron_ingot + 2 redstone'),
        att('muzzle_silencer_phantom_s1',  'Phantom S1 Silencer',       '16 iron_ingot + 6 leather + 2 redstone'),
        att('muzzle_silencer_ptilopsis',   'Ptilopsis Silencer',        '14 iron_ingot + 2 redstone'),
        att('muzzle_silencer_sg',          'SG Silencer',               '18 iron_ingot + 5 leather + 2 redstone'),
        att('muzzle_silencer_ursus',       'Ursus Silencer',            '16 iron_ingot + 6 leather + 2 redstone'),
        att('muzzle_silencer_vulture',     'Vulture Silencer',          '16 iron_ingot + 6 leather + 2 redstone'),
        att('muzzle_silencer_wraith',      'Wraith Silencer',           '10 iron_ingot + 4 leather + 2 white_wool'),
    ]),
    Chapter('att_grips', 'Attachments: Grips', group='Attachments', icon='att:grip_td', order=3, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Grip', note=ATT_NOTE, quests=[
        att('grip_cobra',                  'Cobra Grip',                '10 iron_ingot + 6 leather'),
        att('grip_magpul_afg_2',           'Magpul AFG 2 Grip',         '10 iron_ingot + 4 leather'),
        att('grip_osovets_black',          'Osovets Black Grip',        '10 iron_ingot + 4 leather'),
        att('grip_rk0',                    'RK0 Grip',                  '11 iron_ingot + 4 leather'),
        att('grip_rk1_b25u',               'RK1 B25U Grip',             '16 iron_ingot + 5 leather'),
        att('grip_rk6',                    'RK6 Grip',                  '2 iron_ingot + 1 leather'),
        att('grip_se_5',                   'SE 5 Grip',                 '10 iron_ingot + 4 leather'),
        att('grip_td',                     'TD Grip',                   '10 iron_ingot + 4 leather'),
        att('grip_vertical_military',      'Vertical Military Grip',    '14 iron_ingot + 5 leather'),
        att('grip_vertical_ranger',        'Vertical Ranger Grip',      '18 iron_ingot + 6 leather'),
        att('grip_vertical_talon',         'Vertical Talon Grip',       '11 iron_ingot + 4 leather'),
    ]),
    Chapter('att_stocks', 'Attachments: Stocks', group='Attachments', icon='att:stock_ak12', order=4, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Stock', note=ATT_NOTE, quests=[
        att('oem_stock_heavy',             'OEM Heavy Stock',           '12 iron_ingot + 6 leather'),
        att('oem_stock_light',             'OEM Light Stock',           '8 iron_ingot + 2 leather'),
        att('oem_stock_tactical',          'OEM Tactical Stock',        '14 iron_ingot + 4 leather'),
        att('stock_ak12',                  'AK12 Stock',                '14 iron_ingot + 5 leather'),
        att('stock_carbon_bone_c5',        'Carbon Bone C5 Stock',      '12 iron_ingot + 3 leather'),
        att('stock_heavy_spas_12',         'Heavy SPAS 12 Stock',       '18 iron_ingot + 2 gold_ingot + 4 leather'),
        att('stock_hk_slim_line',          'HK Slim Line Stock',        '16 iron_ingot + 5 leather'),
        att('stock_m4ss',                  'M4SS Stock',                '8 iron_ingot + 5 leather'),
        att('stock_militech_b5',           'Militech B5 Stock',         '16 iron_ingot + 5 leather'),
        att('stock_moe',                   'MOE Stock',                 '12 iron_ingot + 5 leather'),
        att('stock_ripstock',              'Ripstock Stock',            '12 iron_ingot + 5 leather'),
        att('stock_sba3',                  'SBA3 Stock',                '14 iron_ingot + 5 leather'),
        att('stock_tactical_ar',           'Tactical AR Stock',         '18 iron_ingot + 4 gold_ingot + 4 leather'),
        att('stock_tactical_spas_12',      'Tactical SPAS 12 Stock',    '16 iron_ingot + 3 leather'),
    ]),
    Chapter('att_magazines', 'Attachments: Magazines', group='Attachments', icon='att:extended_mag_3', order=5, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Magazine', note=ATT_NOTE, quests=[
        att('extended_mag_1',              'Extended Mag I',            '16 iron_ingot + 4 gold_ingot'),
        att('extended_mag_2',              'Extended Mag II',           '20 iron_ingot + 8 gold_ingot + 8 lapis_lazuli'),
        att('extended_mag_3',              'Extended Mag III',          '32 iron_ingot + 12 gold_ingot + 3 diamond'),
        att('light_extended_mag_1',        'Light Extended Mag I',      '8 iron_ingot'),
        att('light_extended_mag_2',        'Light Extended Mag II',     '12 iron_ingot + 8 lapis_lazuli'),
        att('light_extended_mag_3',        'Light Extended Mag III',    '16 iron_ingot + 8 lapis_lazuli + 4 quartz'),
        att('shotgun_extended_mag_1',      'Shotgun Extended Mag I',    '10 iron_ingot'),
        att('shotgun_extended_mag_2',      'Shotgun Extended Mag II',   '16 iron_ingot + 2 gold_ingot'),
        att('shotgun_extended_mag_3',      'Shotgun Extended Mag III',  '24 iron_ingot + 5 gold_ingot + 8 lapis_lazuli'),
        att('sniper_extended_mag_1',       'Sniper Extended Mag I',     '18 iron_ingot + 6 gold_ingot'),
        att('sniper_extended_mag_2',       'Sniper Extended Mag II',    '26 iron_ingot + 12 gold_ingot + 12 lapis_lazuli'),
        att('sniper_extended_mag_3',       'Sniper Extended Mag III',   '36 iron_ingot + 16 gold_ingot + 8 quartz + 5 diamond'),
    ]),
    Chapter('att_lasers', 'Attachments: Lasers', group='Attachments', icon='att:laser_nightstick', order=6, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Laser', note=ATT_NOTE, quests=[
        att('laser_compact',               'Compact Laser',             '6 iron_ingot + 4 redstone'),
        att('laser_lopro',                 'Lopro Laser',               '10 iron_ingot + 4 redstone'),
        att('laser_nightstick',            'Nightstick Laser',          '4 iron_ingot + 4 redstone'),
        att('laser_peq6',                  'PEQ6 Laser',                '16 iron_ingot + 4 redstone + 1 amethyst_shard'),
    ]),
    Chapter('att_specials', 'Attachments: Specials', group='Attachments', icon='att:bayonet_m9', order=7, repeat=True, auto='no_toast', layout=Grid(cols=6), sub='Special', note=ATT_NOTE, quests=[
        att('ammo_mod_fmj',                'Ammo Mod: FMJ',             '2 crying_obsidian + 5 diamond'),
        att('ammo_mod_he',                 'Ammo Mod: HE',              '3 crying_obsidian + 1 end_crystal'),
        att('ammo_mod_hp',                 'Ammo Mod: HP',              '3 crying_obsidian + 8 gold_ingot'),
        att('ammo_mod_i',                  'Ammo Mod: I',               '2 crying_obsidian + 1 fire_charge + 4 blaze_rod'),
        att('ammo_mod_slug',               'Ammo Mod: Slug',            '3 crying_obsidian + 1 netherite_scrap'),
        att('bayonet_6h3',                 '6H3 Bayonet',               '8 iron_ingot + 4 stick'),
        att('bayonet_m9',                  'M9 Bayonet',                '10 iron_ingot + 4 stick'),
        att('deagle_golden_long_barrel',   'Deagle Golden Long Barrel', '30 gold_ingot + 10 iron_ingot'),
    ]),
]

if __name__ == "__main__":
    main(CHAPTERS, BOOKS, NAMES)
