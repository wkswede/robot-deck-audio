# Robot: a local AI deck music assistant

I wanted one-tap deck music from my phone, watch, or laptop — powered by a local LLM on a Mac mini.

So I built **Robot**, a home-lab music assistant that combines **Open WebUI + Ollama + Flask + AppleScript + Airfoil + Chrome + Apple Shortcuts**.

Now I can say or tap **“Play Deck Music”** and Robot:

1. Connects my **Backyard** speakers in Airfoil
2. Opens my **Deck Music** YouTube playlist in Chrome
3. Clicks YouTube’s **Play all** button via injected JavaScript
4. Starts music outside
5. Lets me pause, skip, or shut everything off from my phone, watch, or Open WebUI

![Robot deck setup](./README-assets:/IMG_4423.jpg)

---

## What it does

Robot currently supports:

* **Play Deck Music**
* **Play/Pause Music**
* **Next Track**
* **Turn on Backyard speakers**
* **Turn on Backyard + Living Room speakers**
* **Turn off Backyard**
* **Turn off all speakers**
* **List Airfoil speakers**

The fun part is that there are **multiple ways to control the same system**:

* **Open WebUI chat** (`"Play deck music"`)
* **Apple Shortcuts** on iPhone / Apple Watch
* **Raycast** shortcut to open Robot from Mac
* direct HTTP calls to Flask for testing/debugging

---

## Architecture

At a high level, the system looks like this:

```text
Apple Shortcut / Open WebUI / Raycast
                ↓
            Flask API
                ↓
      shell scripts + AppleScript
                ↓
    Airfoil + Chrome + YouTube
                ↓
 Backyard / Living Room / Deck speakers
```

### In practice

* **Open WebUI** runs on the Mac mini and exposes tool calls like `play_deck_music()`
* those tool calls hit a **Flask API** running on port `5055`
* Flask routes trigger **shell scripts**
* shell scripts use **AppleScript** to control **Airfoil** and **Google Chrome**
* Chrome opens a YouTube playlist and executes JavaScript to click **Play all**
* Airfoil handles routing the audio to the correct speakers

---

## Hardware / setup

The current backyard setup includes:

* **Mac mini (“Robot”)** — local AI + automation brain
* **Klipsch outdoor speakers** mounted under the eaves
* **Airfoil** for audio routing
* **Google Chrome** as the playback source
* **Deck box** housing parts of the outdoor audio setup
* **Apple Shortcuts** on iPhone / Apple Watch for quick controls

Inside the deck box I’ve got a collection of audio gear, cabling, power, and ventilation. It’s not a polished product build — it’s a home-lab / backyard system that became genuinely useful.

![Inside the deck box](./README-assets:/IMG_4424.jpg)

---

## Key idea: AI doesn’t choose the music

One design choice I like is that Robot does **not** try to become a DJ.

I still curate the playlist myself from my phone. Robot’s job is the activity layer:

* route the right speakers
* open the right playlist
* start playback
* pause / skip / shut it all down

That keeps the system simple and makes it feel more reliable.

---

## Example controls

### Open WebUI

Examples of commands I can give Robot:

* `"Play deck music"`
* `"Pause the music"`
* `"Skip this song"`
* `"Turn on the backyard and living room"`
* `"Turn everything off"`

### Apple Shortcuts

I currently have shortcuts like:

* 🎵 **Play Deck Music**
* ⏯ **Play/Pause Music**
* ⏭ **Next Track**
* 🔇 **All Off**
* 🤖 **Robot** (opens Open WebUI)

### Raycast

I also have a Raycast command that opens Robot instantly from my Mac.

---

## Networking lessons learned

One subtle but important lesson was **where Flask is listening**.

Originally I had Flask running like this:

```python
app.run(host="127.0.0.1", port=5055)
```

That worked from the Mac mini itself and from Open WebUI running in Docker, but **did not work from iPhone Safari / Apple Shortcuts**.

Changing to:

```python
app.run(host="0.0.0.0", port=5055)
```

allowed devices on my LAN to reach the API at:

```text
http://192.168.x.x:5055
```

That was the key to getting Apple Shortcuts working.

### The three URLs that matter

Depending on where the request originates:

* **Robot itself**
  `http://127.0.0.1:5055`

* **Open WebUI container**
  `http://host.docker.internal:5055`

* **iPhone / Apple Shortcuts / other LAN devices**
  `http://192.168.x.x:5055`

That ended up being one of the most useful “glue code” lessons in the project.

---

## API design lesson: long-running actions should return quickly

Some actions — especially **Play Deck Music** — are slow by nature:

* turn on Airfoil speakers
* open Chrome
* load the playlist
* click **Play all**
* wait for music to start

For Apple Shortcuts, it’s better if those endpoints return immediately and let the work continue in the background. In practice, that means using `subprocess.Popen()` for long-running routes rather than blocking on `subprocess.run()`.

For example, the `play_pause` route looks like this:

```python
@app.route("/music/play_pause", methods=["POST"])
def play_pause():
    subprocess.Popen(
        [SCRIPTS["play_pause_music"]],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return jsonify({
        "action": "play_pause_music",
        "status": "started"
    })
```

---

## What’s hacky

Plenty.

* This is very much a **Mac mini + scripts + AppleScript + local AI** project, not a polished product
* YouTube automation is inherently a little brittle
* local models sometimes need a nudge to use the tool instead of talking about the tool
* the deck box contains a bunch of real-world compromise and “figure it out as you go” engineering

But that’s also why I like it. It’s not pretending to be a smart home platform — it’s a useful, very personal home-lab system.

---

## What’s next

A few ideas I want to explore next:

* volume up / volume down
* better “what’s currently playing?” support
* more robust multi-zone presets
* tighter Apple Watch controls
* physical buttons outside
* better prompting / tool descriptions so the local model chooses the right tool more reliably

---

## Why I built it

Because I wanted a computer in my house that does something actually useful.

Not “summarize the internet.”
Not “answer generic questions.”
Just:

> **turn on the deck music and make the backyard feel alive**

And now it does.

---

## Repo structure

Example layout:

```text
robot-actions/
├── airfoil/
│   ├── backyard-chrome-on.sh
│   ├── backyard-living-room-on.sh
│   ├── backyard-off.sh
│   ├── all-off.sh
│   ├── play-deck-music.sh
│   ├── play-pause-music.sh
│   └── next-track.sh
├── server/
│   └── airfoil_server.py
└── README-assets/
    ├── deck-wide.jpg
    └── deck-box-inside.jpg
```

---

## Notes for anyone adapting this

If you want to build something similar, I’d recommend:

* keep your playlist URL in an environment variable or config file
* separate **fast controls** (Shortcuts) from **flexible controls** (chat)
* make the AI control **activities**, not everything
* expect a bit of glue work between networking, browser automation, and audio routing

If you’re a home-lab person, that’s half the fun anyway.
