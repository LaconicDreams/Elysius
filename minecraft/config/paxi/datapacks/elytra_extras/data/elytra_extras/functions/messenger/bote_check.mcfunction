# as a Bote (trader): if his player is gone (offline, scene over), he leaves
function elytra_extras:messenger/tag_owner
execute unless entity @a[tag=mes_cur,tag=mes_scene] on vehicle if entity @s[tag=!mes_leaving] at @s run function elytra_extras:messenger/depart
