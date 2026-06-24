#!/bin/zsh

osascript <<'APPLESCRIPT'
tell application "Google Chrome"
    execute active tab of front window javascript "
var v = document.querySelector('video');
if (v.paused) {
    v.play();
} else {
    v.pause();
}
"
end tell
APPLESCRIPT
