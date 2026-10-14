# rank 7: Gefährte des Boten
team join rang_7 @s
title @s times 10 70 20
title @s subtitle {"text": "Rang 7", "color": "gray"}
title @s title {"text": "Gefährte des Boten", "color": "gold", "bold": true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1.0 0.8
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr steigt auf, Gefährte des Boten. Die Zeit vergisst nicht, wer ihr dient.", "color": "#FFE9A8", "italic": true, "bold": false}]
