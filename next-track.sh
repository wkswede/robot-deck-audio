#!/bin/zsh

osascript <<'APPLESCRIPT'
tell application "Google Chrome"
    execute active tab of front window javascript "
var nextButton = document.querySelector('.ytp-next-button');
if (nextButton) {
    nextButton.click();
    'next clicked';
} else {
    'next button not found';
}
"
end tell
APPLESCRIPT
