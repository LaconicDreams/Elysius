# rank 5: Siegelträger
team join rang_5 @s
title @s times 10 70 20
title @s subtitle {"text": "Rang 5", "color": "gray"}
title @s title {"text": "Siegelträger", "color": "aqua", "bold": true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1.0 0.8
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr steigt auf, Siegelträger. Die Zeit vergisst nicht, wer ihr dient.", "color": "#FFE9A8", "italic": true, "bold": false}]
