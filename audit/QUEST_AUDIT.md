# Quest-Audit Elysius (nur gelesen, nichts geändert)

Stand: Dateien in `minecraft/config/ftbquests/quests`, erzeugt von `audit/audit_quests.py`.

## Zusammenfassung
- 26 Kapitel, **299 Quests**, davon 202 wiederholbar.
- **202 Shop-Quests = 67.6 %** aller Quests; nur 97 Quests sind keine Shop-Einträge.
- Shop schrumpft auf 175 (Einzel+Stack zusammen), 170 (+ Kaliber ohne Waffe raus), 22 (+ Waffen und Aufsätze raus).
- Story hat erst 6 Quests (3 'Zwischen den Zeiten' + 3 Boss-Dungeons).
- 43 Nicht-Story-Quests geben Waffen, Aufsätze oder große Belohnungen (Abschnitt 5).
- 4 Waffen/Aufsätze werden von mehreren Quests verschenkt; 9 Ziele sind echt doppelt (z. B. End City, Enderdrache, Nether/End betreten).
- 5 Munitionssorten im Shop haben keine Waffe (tacz:46x30, tacz:545x39, tacz:68x51fury, tacz:762x25, tacz:762x54).
- Verwaiste Abhängigkeiten: 0, Quests ohne Aufgabe: 0, ohne Belohnung: 0, kaputte Aufgabenziele: 0.
- order_index doppelt innerhalb einer Gruppe: 0.
- Alle Kapitel werden von `questtools/questgen.py` erzeugt: Streichungen später dort machen, nicht in den .snbt.

## 1. Inventar
Belohnungen = Anzahl Belohnungs-Einträge in den Dateien (große Munitionsmengen sind oft auf 2 bis 4 Einträge verteilt).

| Datei | Titel | Gruppe | order | Quests | wiederholbar | Waffe | Munition | Aufsatz | Raketen | Shulker | Sonstiges |
|---|---|---|---|---|---|---|---|---|---|---|---|
| att_sights.snbt | Attachments: Sights | Attachments | 0 | 18 | 18 | 0 | 0 | 18 | 0 | 0 | 0 |
| att_scopes.snbt | Attachments: Scopes | Attachments | 1 | 12 | 12 | 0 | 0 | 12 | 0 | 0 | 0 |
| att_muzzles.snbt | Attachments: Muzzles | Attachments | 2 | 16 | 16 | 0 | 0 | 16 | 0 | 0 | 0 |
| att_grips.snbt | Attachments: Grips | Attachments | 3 | 11 | 11 | 0 | 0 | 11 | 0 | 0 | 0 |
| att_stocks.snbt | Attachments: Stocks | Attachments | 4 | 14 | 14 | 0 | 0 | 14 | 0 | 0 | 0 |
| att_magazines.snbt | Attachments: Magazines | Attachments | 5 | 12 | 12 | 0 | 0 | 12 | 0 | 0 | 0 |
| att_lasers.snbt | Attachments: Lasers | Attachments | 6 | 4 | 4 | 0 | 0 | 4 | 0 | 0 | 0 |
| att_specials.snbt | Attachments: Specials | Attachments | 7 | 8 | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| overworld.snbt | Overworld Bounties | Dimensions | 0 | 5 | 0 | 5 | 7 | 0 | 5 | 0 | 0 |
| nether.snbt | Nether Bounties | Dimensions | 1 | 5 | 0 | 4 | 9 | 0 | 5 | 0 | 0 |
| aether.snbt | Aether Hunts | Dimensions | 2 | 5 | 0 | 4 | 6 | 0 | 5 | 0 | 0 |
| the_end.snbt | End Trophies | Dimensions | 3 | 5 | 0 | 4 | 6 | 0 | 5 | 0 | 0 |
| start_here.snbt | Start Here | Quests | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 2 |
| story_ashen_skyways.snbt | Zwischen den Zeiten | Quests | 1 | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 2 |
| elytra_start.snbt | Taking Flight | Quests | 2 | 15 | 0 | 4 | 14 | 0 | 18 | 0 | 6 |
| good_deeds.snbt | Good Deeds | Quests | 3 | 17 | 0 | 0 | 0 | 0 | 0 | 17 | 2 |
| long_term.snbt | Long-Term Goals | Quests | 4 | 19 | 0 | 3 | 13 | 3 | 0 | 0 | 27 |
| backpack_upgrades.snbt | Backpack Upgrades | Quests | 5 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| boss_dungeons.snbt | Boss Dungeons | Quests | 6 | 3 | 0 | 3 | 5 | 0 | 0 | 0 | 0 |
| horde_leaders.snbt | Horde Leaders | Quests | 7 | 8 | 0 | 0 | 8 | 6 | 0 | 0 | 2 |
| gun_shop.snbt | Gun Shop | Shop | 0 | 53 | 53 | 53 | 0 | 0 | 0 | 0 | 0 |
| rockets.snbt | Rockets | Shop | 1 | 6 | 6 | 0 | 0 | 0 | 7 | 0 | 0 |
| ammo_pistols_smgs.snbt | Ammo: Pistols and SMGs | Shop | 2 | 18 | 18 | 0 | 18 | 0 | 0 | 0 | 0 |
| ammo_rifles.snbt | Ammo: Rifles | Shop | 3 | 16 | 16 | 0 | 16 | 0 | 0 | 0 | 0 |
| ammo_heavy.snbt | Ammo: Snipers and Heavy | Shop | 4 | 8 | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| ammo_shotguns_launchers.snbt | Ammo: Shotguns and Launchers | Shop | 5 | 6 | 6 | 0 | 6 | 0 | 0 | 0 | 0 |
| **Summe** | 26 Kapitel |  |  | 299 | 202 | 80 | 117 | 104 | 46 | 17 | 52 |

## 2. Kategorien
| Kategorie | Quests |
|---|---|
| Shop | 202 |
| Nebenquest | 57 |
| Meilenstein | 25 |
| Story | 6 |
| Tutorial/Einstieg | 5 |
| Füller | 4 |

Regeln: Story = 'Zwischen den Zeiten' + Boss Dungeons. Shop = wiederholbar, verbraucht nur Items, gibt nur Items. Tutorial = Start Here + die erste Kette in Taking Flight. Meilenstein = Dimension betreten, Boss/Vanilla-Boss, Stufen (Flugstrecke, Kills), Finale. Nebenquest = Kill-Bounties, Good Deeds, Rucksack-Upgrades, einzelne Anführer, Strukturen. Füller = Spielzeit-Quests (verlangen keine Handlung). Pro Quest: `quests.csv`.

| Kapitel | Kategorien |
|---|---|
| aether.snbt | Nebenquest: 4, Meilenstein: 1 |
| ammo_heavy.snbt | Shop: 8 |
| ammo_pistols_smgs.snbt | Shop: 18 |
| ammo_rifles.snbt | Shop: 16 |
| ammo_shotguns_launchers.snbt | Shop: 6 |
| att_grips.snbt | Shop: 11 |
| att_lasers.snbt | Shop: 4 |
| att_magazines.snbt | Shop: 12 |
| att_muzzles.snbt | Shop: 16 |
| att_scopes.snbt | Shop: 12 |
| att_sights.snbt | Shop: 18 |
| att_specials.snbt | Shop: 8 |
| att_stocks.snbt | Shop: 14 |
| backpack_upgrades.snbt | Nebenquest: 11 |
| boss_dungeons.snbt | Story: 3 |
| elytra_start.snbt | Meilenstein: 6, Nebenquest: 5, Tutorial/Einstieg: 4 |
| good_deeds.snbt | Nebenquest: 16, Meilenstein: 1 |
| gun_shop.snbt | Shop: 53 |
| horde_leaders.snbt | Nebenquest: 6, Meilenstein: 2 |
| long_term.snbt | Meilenstein: 13, Füller: 4, Nebenquest: 2 |
| nether.snbt | Nebenquest: 4, Meilenstein: 1 |
| overworld.snbt | Nebenquest: 5 |
| rockets.snbt | Shop: 6 |
| start_here.snbt | Tutorial/Einstieg: 1 |
| story_ashen_skyways.snbt | Story: 3 |
| the_end.snbt | Nebenquest: 4, Meilenstein: 1 |

## 3. Empfehlung je Kapitel
| Kapitel | Empfehlung | Grund |
|---|---|---|
| att_sights.snbt | später streichen | Aufsätze gibt es auch in Dungeon-Truhen; die 95 Aufsatz-Quests machen den Quest-Baum unübersichtlich. |
| att_scopes.snbt | später streichen | Siehe Sights. |
| att_muzzles.snbt | später streichen | Siehe Sights. |
| att_grips.snbt | später streichen | Siehe Sights. |
| att_stocks.snbt | später streichen | Siehe Sights. |
| att_magazines.snbt | später streichen | Siehe Sights. |
| att_lasers.snbt | später streichen | Siehe Sights. |
| att_specials.snbt | später streichen | Ammo-Mods (FMJ/HE/HP/I/Slug) sind stark und eher Story- oder Boss-Belohnungen. |
| overworld.snbt | zusammenlegen | Vier kleine Bounty-Kapitel mit je 5 Quests lassen sich zu einem Kapitel 'Bounties' zusammenlegen. |
| nether.snbt | zusammenlegen | Wie Overworld: 5 Kill-Bounties, jede mit Waffe; gemeinsam mit den anderen Dimensionen. |
| aether.snbt | zusammenlegen | Wie Overworld; der Aether passt aber thematisch zum alten Pfad der Story. |
| the_end.snbt | zusammenlegen | Wie Overworld; doppelt End City und Drachen mit Taking Flight. |
| start_here.snbt | behalten | Einziger Einstieg (Elytra, Raketen, Rucksack), die Story baut darauf auf. |
| story_ashen_skyways.snbt | behalten | Hauptstrang, hier sollen die großen Belohnungen hin. |
| elytra_start.snbt | kürzen | Einstiegskette ist gut, aber die 'Hard'-Bosse doppeln End Trophies / Long-Term und geben Waffen außerhalb der Story. |
| good_deeds.snbt | kürzen | 16 Quests spiegeln nur Vanilla-Advancements 1:1 mit derselben Belohnungsart (Shulker); eine Auswahl plus Finale reicht. |
| long_term.snbt | kürzen | Stufenketten sind okay, aber Spielzeit-Quests sind Füller und die Boss-Kills passen besser in die Story. |
| backpack_upgrades.snbt | behalten | Jede Quest gibt ein eigenes, sonst knappes Upgrade, überschaubar. |
| boss_dungeons.snbt | in die Story verschieben | Laut Plan sind die Boss-Dungeons die Siegel des Hauptstrangs. |
| horde_leaders.snbt | in die Story verschieben | Eigene Mechanik des Packs; die Anführer eignen sich als Story-Gegner (z. B. Eintreiber des Boten). |
| gun_shop.snbt | später streichen | 53 Waffen gegen Erz untergraben Waffen als Story-Belohnung; erst nach fertiger Story streichen. |
| rockets.snbt | kürzen | Raketen sind für Elytra wichtig; Einzel- und Bulk-Version je Währung zusammenlegen. |
| ammo_pistols_smgs.snbt | kürzen | Einzel + Stack je Kaliber zusammenlegen, Kaliber ohne Waffe streichen. |
| ammo_rifles.snbt | kürzen | Einzel + Stack je Kaliber zusammenlegen, Kaliber ohne Waffe streichen. |
| ammo_heavy.snbt | kürzen | Einzel + Stack je Kaliber zusammenlegen. |
| ammo_shotguns_launchers.snbt | kürzen | Einzel + Stack je Kaliber zusammenlegen. |

Auffällige Einzelfälle: siehe Abschnitt 5 und 6 sowie `DELETE_CANDIDATES.md`.

## 4. Shop-Analyse
- Shop-Quests: **202 von 299 (67.6 %)**.
- Kapitel: ammo_heavy.snbt (8), ammo_pistols_smgs.snbt (18), ammo_rifles.snbt (16), ammo_shotguns_launchers.snbt (6), att_grips.snbt (11), att_lasers.snbt (4), att_magazines.snbt (12), att_muzzles.snbt (16), att_scopes.snbt (12), att_sights.snbt (18), att_specials.snbt (8), att_stocks.snbt (14), gun_shop.snbt (53), rockets.snbt (6).

| Schritt (aufeinander aufbauend) | Shop-Quests | Anteil an heutiger Gesamtzahl | Quests gesamt danach |
|---|---|---|---|
| heute | 202 | 67.6 % | 299 |
| (a) Einzel + Stack je Item/Währung zu einer Quest | 175 | 58.5 % | 272 |
| (b) Munition: 1 Quest pro Kaliber, Kaliber ohne Waffe gestrichen | 170 | 56.9 % | 267 |
| (c) zusätzlich Waffen und Aufsätze ganz entfernt | 22 | 7.4 % | 119 |

- Nach (a) bleiben je Art: attachment: 95, modern_kinetic_gun: 53, ammo: 24, firework_rocket: 3.
- Nur (c) ohne (a)/(b): 54 Shop-Quests (Waffen und Aufsätze raus, Munition/Raketen unverändert).
- (b) erklärt: nach (a) gibt es schon genau 1 Quest pro Kaliber; 'wenige' heißt hier zusätzlich: Kaliber, die laut Untertitel keine Waffe nutzt, fallen weg (5).

## 5. Belohnungs-Check (Waffen, Aufsätze, große Belohnungen außerhalb der Story)
| Kapitel | Quest | Belohnung | Vorschlag |
|---|---|---|---|
| aether.snbt | Zephyr Chase | 1x tacz:vector45 | Aether = alter Pfad der Story; Zephyr-Jagd als Story-Schritt, Waffe ggf. durch Aether-Item ersetzen. |
| aether.snbt | Stone Cold | 1x tacz:m870 | Wie Zephyr Chase. |
| aether.snbt | Sentry Shutdown | 1x tacz:m4a1 | M4A1 doppelt (auch Dragon Slayer): eine Vergabe streichen. |
| aether.snbt | Gatekeeper | 1x tacz:spr15hb | Slider ist ein Aether-Boss: guter Story-Meilenstein des alten Pfads. |
| boss_dungeons.snbt | Ash to Ash | 1x tacz:scar_l | Schon Siegel-Kandidat (Boss Dungeons). |
| boss_dungeons.snbt | Eye of the Storm | 1x tacz:m107 | Schon Siegel-Kandidat (Boss Dungeons). |
| boss_dungeons.snbt | Into the Hollow | 1x tacz:fn_evolys | Schon Siegel-Kandidat (Boss Dungeons). |
| elytra_start.snbt | Target Practice | 1x tacz:m1911 | Bleibt Tutorial; M1911 als Startwaffe ist okay, könnte aber Teil des modernen Pfads werden. |
| elytra_start.snbt | Sky's the Limit | 1x minecraft:netherite_chestplate | Netherite-Brustplatte ist sehr groß für 'Elytra finden' (man startet mit Elytra); kleiner machen. |
| elytra_start.snbt | Ghast Hunter | 1x tacz:ak47 | AK-47 raus, stattdessen Story-Item (z. B. Ghast-Träne als Zutat für eine Bote-Aufgabe). |
| elytra_start.snbt | Deep Dark Delve | 1x tacz:m700 | Ancient City als Story-Ort (alter Pfad); M700 als Belohnung dort statt in Taking Flight. |
| elytra_start.snbt | Wither Sky | 2x minecraft:netherite_ingot | Großer Story-Meilenstein (Nether-Kapitel des alten Pfads); Netherite dort vergeben. |
| elytra_start.snbt | Dragon Slayer | 1x tacz:m4a1, 4x minecraft:netherite_ingot | Doppelt mit 'Dragon's End': Drachen als Story-Finale eines Akts, eine Quest streichen. |
| good_deeds.snbt | Pillar of the Community | 1x minecraft:totem_of_undying | Totem + 16 Smaragde: okay als Nebenfinale, könnte Bote-Bezug bekommen ('gute Taten'). |
| horde_leaders.snbt | Läufer | 1x tacz:muzzle_choke_sg | Anführer als Bote-'Eintreiber' in die Story; Aufsatz als Belohnung passt. |
| horde_leaders.snbt | Brecher | 1x tacz:ammo_mod_fmj | Wie Läufer. |
| horde_leaders.snbt | Spucker | 1x tacz:scope_standard_8x | Wie Läufer. |
| horde_leaders.snbt | Schreier | 1x tacz:muzzle_silencer_ptilopsis | Wie Läufer. |
| horde_leaders.snbt | Kriecher | 1x tacz:laser_peq6 | Wie Läufer. |
| horde_leaders.snbt | Leader Hunter | 1x tacz:ammo_mod_he | HE-Mod + .50 BMG: guter Story-Meilenstein 'alle Eintreiber besiegt'. |
| long_term.snbt | Skyward Bound | 1x minecraft:netherite_ingot | Netherite für Flugstrecke: okay, ggf. kleiner. |
| long_term.snbt | Sky Legend | 1x tacz:minigun, 4x minecraft:netherite_ingot | Minigun + 4 Netherite: als Story-Endbelohnung geeigneter als für Flugstrecke. |
| long_term.snbt | Hunter III | 1x tacz:hk416d | HK416D raus, Diamanten/Smaragde lassen. |
| long_term.snbt | Hunter IV | 1x tacz:deagle_golden, 2x minecraft:netherite_ingot | Golden Desert Eagle als Story-Trophäe (z. B. nach allen Siegeln). |
| long_term.snbt | Deep Warden | 1x tacz:ammo_mod_he, 2x minecraft:netherite_ingot | Warden als optionales Siegel; HE-Mod passt dorthin. |
| long_term.snbt | Sun Spirit | 1x tacz:ammo_mod_i | Aether-Endboss: Story-Meilenstein des alten Pfads. |
| long_term.snbt | Valkyrie Queen | 1x tacz:ammo_mod_hp | Aether-Boss: Story-Meilenstein des alten Pfads. |
| long_term.snbt | Monster Hunter | 1x minecraft:totem_of_undying, 2x minecraft:enchanted_golden_apple | Totem + 2 verzauberte Goldäpfel: als Long-Term okay, sonst Story-Finale. |
| long_term.snbt | Mansion Raider | 1x minecraft:totem_of_undying | Waldanwesen als möglicher Story-Ort (Illager = 'Eintreiber'); sonst als Nebenquest okay. |
| long_term.snbt | Sky Dweller | 1x minecraft:netherite_ingot | Netherite nur für Spielzeit: Belohnung kleiner oder Quest streichen (Füller). |
| nether.snbt | Blaze Runner | 1x tacz:ak47 | AK-47 doppelt (auch Ghast Hunter): eine Vergabe streichen. |
| nether.snbt | Bone Crusher | 1x tacz:aa12 | Wither-Skelette passen zum Ashen-Warlord-Siegel; AA-12 als Story-Belohnung dort. |
| nether.snbt | Hoglin Hunt | 1x tacz:m249 | M249 ist eine Emerald-Waffe: besser Story-Belohnung (Nether-Akt). |
| nether.snbt | Brute Force | 1x tacz:m700 | M700 doppelt (auch Deep Dark Delve): eine Vergabe streichen. |
| overworld.snbt | Zombie Stopper | 1x tacz:glock_17 | Glock 17 als Belohnung des modernen Pfads (Kupfer/9mm) statt als Bounty. |
| overworld.snbt | Web Cutter | 1x tacz:db_short | Bounty behalten, Waffe durch Munition/Raketen ersetzen. |
| overworld.snbt | Creeper Crowd | 1x tacz:uzi | Bounty behalten, Waffe durch Munition/Raketen ersetzen. |
| overworld.snbt | Raid Breaker | 1x tacz:hk_mp5a5 | Passt als Story-Schritt (Dorf verteidigen, Bote-Wunsch 'Macht'); MP5 dort vergeben. |
| overworld.snbt | Beast Slayer | 1x tacz:sks_tactical | Bounty behalten, Waffe durch Munition ersetzen. |
| the_end.snbt | Enderman Ambush | 1x tacz:scar_h | SCAR-H als End-Belohnung in die Story verschieben oder durch Munition ersetzen. |
| the_end.snbt | Shell Game | 1x tacz:aug | Bounty behalten, Waffe durch Munition/Shulker-Schalen ersetzen. |
| the_end.snbt | End City Raid | 1x tacz:ai_awp | Doppelt vorhanden (Taking Flight + End Trophies): eine davon streichen, die andere in die Story. |
| the_end.snbt | Dragon's End | 1x tacz:m95 | Siehe Dragon Slayer. |

## 6. Überschneidungen
### Gleiche Waffe/Aufsatz von mehreren Quests (ohne Shop)
| Item | Anzahl | Quests |
|---|---|---|
| tacz:ak47 | 2 | Ghast Hunter (elytra_start); Blaze Runner (nether) |
| tacz:ammo_mod_he | 2 | Leader Hunter (horde_leaders); Deep Warden (long_term) |
| tacz:m4a1 | 2 | Sentry Shutdown (aether); Dragon Slayer (elytra_start) |
| tacz:m700 | 2 | Deep Dark Delve (elytra_start); Brute Force (nether) |

Zusätzlich ist **jede** als Quest-Belohnung vergebene Waffe auch im Gun Shop kaufbar.

### Gleiches Ziel (gleicher Aufgabentyp + Ziel, ohne Shop)
Bei `stat` steht der Zielwert dabei; unterschiedliche Werte sind Stufen, keine echten Doppelungen.

| Ziel | Anzahl | Bewertung | Quests |
|---|---|---|---|
| advancement modpack:leaders/kill_brecher | 2 | Sammel-Quest (gewollt) | Brecher (horde_leaders); Leader Hunter (horde_leaders) |
| advancement modpack:leaders/kill_kriecher | 2 | Sammel-Quest (gewollt) | Kriecher (horde_leaders); Leader Hunter (horde_leaders) |
| advancement modpack:leaders/kill_laeufer | 2 | Sammel-Quest (gewollt) | Läufer (horde_leaders); Leader Hunter (horde_leaders) |
| advancement modpack:leaders/kill_platzer | 2 | Sammel-Quest (gewollt) | Platzer (horde_leaders); Leader Hunter (horde_leaders) |
| advancement modpack:leaders/kill_schreier | 2 | Sammel-Quest (gewollt) | Schreier (horde_leaders); Leader Hunter (horde_leaders) |
| advancement modpack:leaders/kill_spucker | 2 | Sammel-Quest (gewollt) | Spucker (horde_leaders); Leader Hunter (horde_leaders) |
| dimension minecraft:the_end | 3 | doppelt | Always Stocked (backpack_upgrades); Into the End (elytra_start); The Final Frontier (the_end) |
| dimension minecraft:the_nether | 3 | doppelt | Hot Pocket (backpack_upgrades); Nether Glider (elytra_start); Through the Portal (nether) |
| kill minecraft:blaze | 2 | doppelt | Forge on Your Back (backpack_upgrades, 15); Blaze Runner (nether, 10) |
| kill minecraft:ender_dragon | 2 | doppelt | Dragon Slayer (elytra_start, 1); Dragon's End (the_end, 1) |
| kill minecraft:enderman | 2 | doppelt | Black Hole (backpack_upgrades, 10); Enderman Ambush (the_end, 10) |
| kill minecraft:phantom | 2 | doppelt | Gravity Well (backpack_upgrades, 10); Night Sky Hunter (elytra_start, 5) |
| kill minecraft:skeleton | 2 | doppelt | Portable Workbench (backpack_upgrades, 20); Target Practice (elytra_start, 3) |
| kill minecraft:zombie | 2 | doppelt | Sticky Fingers (backpack_upgrades, 25); Zombie Stopper (overworld, 10) |
| stat minecraft:aviate_one_cm | 7 | Stufen (gewollt) | First Flight (elytra_start, 100000); Scenic Route (elytra_start, 500000); Long Haul (elytra_start, 1000000); Frequent Flyer (long_term, 2500000); Cross-Country (long_term, 5000000); Skyward Bound (long_term, 10000000); Sky Legend (long_term, 25000000) |
| stat minecraft:mob_kills | 4 | Stufen (gewollt) | Hunter I (long_term, 250); Hunter II (long_term, 1000); Hunter III (long_term, 2500); Hunter IV (long_term, 5000) |
| stat minecraft:play_time | 4 | Stufen (gewollt) | Settled In (long_term, 720000); Veteran (long_term, 1800000); Lifer (long_term, 3600000); Sky Dweller (long_term, 7200000) |
| structure minecraft:end_city | 2 | doppelt | End City Raid (elytra_start); End City Raid (the_end) |

### Technische Prüfungen
- Verwaiste Abhängigkeiten (ID existiert nicht): 0
- Quests ohne Aufgabe: 0
- Quests ohne Belohnung: 0
- Aufgaben mit unbekanntem Ziel (Advancement/Struktur/Dimension/Mob/Stat/Item nicht gefunden): 0
- Unerreichbare Quests (kaputtes Ziel oder Abhängigkeit darauf): 0
- order_index doppelt innerhalb einer Gruppe: 0
- order_index über Gruppen hinweg gleich (normal, FTB sortiert pro Gruppe): 0: 4x, 1: 4x, 2: 4x, 3: 4x, 4: 3x, 5: 3x, 6: 2x, 7: 2x.
- Nicht prüfbar ohne Spiel: ob 'Long Haul' (Taking Flight) ohne Abhängigkeit absichtlich frei ist; ob die Story-Quests im Spiel wirklich unsichtbar bleiben (Kapitel-Flag `hide_quest_until_deps_complete`).

## 7. Verbindungen Quests <-> Bote / Boss-Dungeons / Horde Leaders
| Kapitel | Quest | Art | Ziel / Quelle |
|---|---|---|---|
| boss_dungeons.snbt | Ash to Ash | Aufgabe structure | elytra_dungeons:ashen_barrow -> Datapack elytra_dungeons (Boss-Dungeons) |
| boss_dungeons.snbt | Ash to Ash | Aufgabe advancement | elytra_dungeons:bosses/ashen_warlord -> Datapack elytra_dungeons (Boss-Dungeons) |
| boss_dungeons.snbt | Eye of the Storm | Aufgabe structure | elytra_dungeons:storm_spire -> Datapack elytra_dungeons (Boss-Dungeons) |
| boss_dungeons.snbt | Eye of the Storm | Aufgabe advancement | elytra_dungeons:bosses/tempest_herald -> Datapack elytra_dungeons (Boss-Dungeons) |
| boss_dungeons.snbt | Into the Hollow | Aufgabe structure | elytra_dungeons:rift_gate -> Datapack elytra_dungeons (Boss-Dungeons) |
| boss_dungeons.snbt | Into the Hollow | Aufgabe advancement | elytra_dungeons:bosses/hollow_magus -> Datapack elytra_dungeons (Boss-Dungeons) |
| horde_leaders.snbt | Cut Off the Head | Aufgabe advancement | modpack:leaders/kill_any -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Läufer | Aufgabe advancement | modpack:leaders/kill_laeufer -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Brecher | Aufgabe advancement | modpack:leaders/kill_brecher -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Spucker | Aufgabe advancement | modpack:leaders/kill_spucker -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Schreier | Aufgabe advancement | modpack:leaders/kill_schreier -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Kriecher | Aufgabe advancement | modpack:leaders/kill_kriecher -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Platzer | Aufgabe advancement | modpack:leaders/kill_platzer -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_laeufer -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_brecher -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_spucker -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_schreier -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_kriecher -> Datapack elytra_hordes (Horde Leaders) |
| horde_leaders.snbt | Leader Hunter | Aufgabe advancement | modpack:leaders/kill_platzer -> Datapack elytra_hordes (Horde Leaders) |
| story_ashen_skyways.snbt | Schwerter und Kugeln | Befehl-Belohnung | /execute as @p at @s run function elytra_extras:messenger/arrive |
| story_ashen_skyways.snbt | Schwerter und Kugeln | Aufgabe advancement | elytra_extras:kackhaufen -> Datapack elytra_extras (Bote/Rezept) |

Weitere Verbindungen (nicht in Quest-Dateien, aber relevant beim Streichen):
- Boss-Advancements werden von `elytra_dungeons/.../victory.mcfunction` per `advancement grant @a[distance=..48/64]` vergeben.
- Horde-Leader-Advancements (`modpack:leaders/*`) lösen beim Töten eines Mobs mit Tag `modpack_horde_leader` aus.
- Bote-Wunsch 'Macht' (Fehlschlag) startet eine Horde über `modpack:horde/start` (Datapack-zu-Datapack, keine Quest).
- Rezept 'Kackhaufen' (Story Q3) braucht 1 Patrone 9mm; Q2 'Kupferpfeil' gibt genau 1 Patrone. Weitere 9mm-Quellen in Quests: Shop '9mm Ammo' und Creeper Crowd, Hunter I, Kupferpfeil, Raid Breaker, Schreier, Sky's the Limit, Zombie Stopper. Fällt der Shop weg, bleibt Q2 die sichere Quelle.
- Datapack-Advancements, die noch keine Quest nutzt: `elytra_extras:bote/kill_player`, `elytra_extras:bote/kill_villager`, `elytra_extras:bote/macht_failed`, `elytra_extras:bote/macht_paid`, `elytra_extras:bote/schutz_endured`, `elytra_extras:bote/wish_macht`, `elytra_extras:bote/wish_schutz`, `elytra_extras:bote/wish_wissen`, `elytra_extras:bote/wissen_survived`, `modpack:leaders/kriecher_grab`.
