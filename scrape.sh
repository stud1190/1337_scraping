#!/bin/bash
## wget --mirror --convert-links -E $@ "https://1337x.to"
httrack -O 1337x 'https://1337x.to' --sockets=8 -p1 --continue --cache=1
