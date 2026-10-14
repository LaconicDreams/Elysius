# As + at the link of a leader that is gone. With a player near it was killed (effects run);
# otherwise it was only unloaded or removed, so it is cleaned up quietly.
execute if entity @a[distance=..64,gamemode=!spectator] run function modpack:leader/on_death
function modpack:leader/unlink
