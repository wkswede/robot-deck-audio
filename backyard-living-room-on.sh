#!/bin/zsh
osascript <<'APPLESCRIPT'
tell application "Airfoil"
    set current audio source to application source "Google Chrome"
    connect to speaker "Backyard"
    connect to speaker "Living Room"
end tell
APPLESCRIPT
