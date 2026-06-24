#!/bin/zsh

PLAYLIST_ID="PL1c4eZB9r1Xe_miSUSGIoOsTpNbchlHdp"
DECK_URL="https://youtube.com/playlist?list=$PLAYLIST_ID"

/Users/robot/robot-actions/airfoil/backyard-chrome-on.sh

sleep 2

osascript <<APPLESCRIPT
tell application "Google Chrome"
    activate
    if (count of windows) = 0 then
        make new window
    end if
    set URL of active tab of window 1 to "$DECK_URL"
end tell
APPLESCRIPT

sleep 6

osascript <<'APPLESCRIPT'
tell application "Google Chrome"
    activate
    execute active tab of front window javascript "document.querySelector('[aria-label=\"Play all\"]').click()"
end tell
APPLESCRIPT
