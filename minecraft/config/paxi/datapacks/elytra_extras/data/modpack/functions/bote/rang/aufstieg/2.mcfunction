# rank 2: Minutenzeiger
team join rang_2 @s
title @s times 10 70 20
title @s subtitle {"text": "Rang 2", "color": "gray"}
title @s title {"text": "Minutenzeiger", "color": "white", "bold": true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1.0 0.8
tellraw @s ["", {"text": "\n✦ Der Bote ✦ » ", "color": "gold", "bold": true}, {"text": "Ihr steigt auf, Minutenzeiger. Die Zeit vergisst nicht, wer ihr dient.", "color": "#FFE9A8", "italic": true, "bold": false}]
