#!/bin/zsh
osascript <<'APPLESCRIPT'
tell application "Airfoil"
    disconnect from every speaker
end tell
APPLESCRIPT
