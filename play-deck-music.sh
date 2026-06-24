#!/bin/zsh

DECK_URL="https://youtube.com/playlist?list=YOUR_PLAYLIST_ID"

# Replace YOUR_PLAYLIST_ID with your own YouTube playlist.

/Users/robot/robot-actions/airfoil/backyard-chrome-on.sh

sleep 2

open -a "Google Chrome" "$DECK_URL"

sleep 6

osascript <<'APPLESCRIPT'
tell application "Google Chrome"
    activate
    execute active tab of front window javascript "document.querySelector('[aria-label=\"Play all\"]').click()"
end tell
APPLESCRIPT
