# STATUS (short running log; full details in CHANGELOG.md)

## 2026-10-14 - Der Bote, step 4: the three wishes
- Backup: backup/bote-wishes-2026-10-14_012031 (all Paxi datapacks, quest chapters, messengergen.py)
- Built into questtools/messengergen.py (CONFIG block "step 4"); generated into config/paxi/datapacks/elytra_extras.
- After the deal: wish question MACHT / SCHUTZ / WISSEN (once per player), price, "Ihr werdet von mir hören.", then the shop.
- Scoreboards: mes_wish (1 Macht, 2 Schutz, 3 Wissen), mes_price (1 open, 2 paid/endured/survived, 3 failed).
- Advancements for FTB Quests: elytra_extras:bote/wish_macht, wish_schutz, wish_wissen, macht_paid, macht_failed,
  schutz_endured, wissen_survived. No quests created.
- Validator: OK. Not yet tested in game.
## 2026-10-14 - Bote silence fix
- Cave sound at intervals removed: the muting sound is now a real silent .ogg (questtools/oggtool.py). Needs a full game restart.

## 2026-10-14 - Bote leaves after the farewell
- 3 s after "Ihr werdet von mir hören." he rides off and vanishes (instead of opening the shop).

## 2026-10-14 - Der Zeitbote, atmosphere and control: step 1 (backup)
- Backup: backup/bote-atmosphere-2026-10-14_015346 (Paxi datapacks + resourcepacks + messengergen.py). Nothing changed yet.
- Checked: AmbientSounds wind events are normal sound events (/playsound works, no extraction); its mixins do not touch vanilla sound volume.

## 2026-10-14 - Quest-Audit (read only)
- New: audit/QUEST_AUDIT.md, audit/quests.csv, audit/DELETE_CANDIDATES.md, audit/audit_quests.py, audit/verify_counts.py.
- 299 quests, 202 shop entries (67.6 %). No quest, datapack or config changed. Counts re-checked by verify_counts.py: OK.
## 2026-10-14 - Der Zeitbote, atmosphere and control: step 2 (built)
- questtools/messengergen.py rebuilt (owner model, seat, music, ambient layer, wind, facing, failsafes, force_end); regenerated.
- Validator: OK (0 errors). /reload in game not yet done (needs the game). Details: CHANGELOG.md.
## 2026-10-14 - Rangsystem: step 1 (backup)
- Backup: backup/ranks-2026-10-14_022512 (Paxi datapacks + messengergen.py).

## 2026-10-14 - Rangsystem: step 2 (built)
- questtools/rankgen.py + messengergen.py regenerated; validator OK (0 errors, 0 warnings). Not tested in game yet.
## 2026-10-14 - Pfad-Belohnungen: step 1 (backup)
- Backup: backup/pfadbelohnungen-2026-10-14_024711 (Paxi datapacks).

## 2026-10-14 - Pfad-Belohnungen: step 2 (built)
- questtools/pathgen.py; all three generators re-run; validator OK (0 errors, 0 warnings). Not tested in game yet.
## 2026-10-14 - Aufräumen (Phase 2, approved: S, W, U, archive, docs/)
- Safety zip backup/cleanup-2026-10-14_234234.zip (checked). 139 candidate paths + 9 old backups -> _to_delete/ (nothing deleted).
- Old backups packed into backup/archive-bis-2026-10-14.zip. Notes moved to docs/ (README and COMMANDS paths updated).
- Instance now 2.03 GB / 8079 files without _to_delete and the safety zip (was 2.39 GB / 13664). Validator OK.
- Report + undo: docs/cleanup/CLEANUP_REPORT.md. Final delete of _to_delete/ only after the user's test.
## 2026-10-14 - Removed jumpscare mods (user request)
- foxy_jumpscare-0.1-1.20.1.jar (+ .index/withered-foxy-jumpscare.pw.toml) and witheredfoxy-2.0.0.jar moved to backup/mods-removed-2026-10-14_234819/. Nothing depended on them.
- 2026-10-14: the user deleted _to_delete/ after the cleanup. Everything from it is still in backup/cleanup-2026-10-14_234234.zip.
- 2026-10-14: backup/cleanup-2026-10-14_234234.zip moved to the Windows Recycle Bin on the user's request (the cleanup can no longer be undone from the instance folder once the bin is emptied).
- 2026-10-14: .packignore now also excludes backup/ (Prism exports no longer include our backups). Old file: backup/packignore-*.bak.
- 2026-10-15: Prism instance icon changed: new PrismLauncher/icons/elysius.png (512x512 PNG), instance.cfg iconKey elytra_pack_icon -> elysius (old cfg in backup/instance.cfg.*.bak; old icon file kept).
