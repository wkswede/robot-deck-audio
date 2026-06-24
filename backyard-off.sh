#!/bin/zsh
osascript <<'APPLESCRIPT'
tell application "Airfoil"
    disconnect from speaker "Backyard"
end tell
APPLESCRIPT
