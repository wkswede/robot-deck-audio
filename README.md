# Robot: A Local AI & AppleScript Backyard Audio Assistant

"Robot" is a Mac Mini-powered home automation hub that orchestrates multi-room outdoor audio and automates YouTube media playback using a local LLM, AppleScript, and native iOS Apple Shortcuts. 

It is beautifully hacky, entirely local-first, subscription-free, and handles home automation without a single byte of telemetry leaving my local network.

## The Main Breakthrough

I can say or tap “Play Deck Music” from an iPhone, Mac, or local chat interface, and Robot automatically executes the entire physical and visual staging sequence:
1. Connects the Backyard speakers via Rogue Amoeba's Airfoil.
2. Opens a curated YouTube playlist in Google Chrome on the host machine.
3. Injects native JavaScript into Chrome to click the YouTube “Play all” button automatically.

## The Architecture

[ iPhone Safari / Apple Shortcuts / Raycast ] (LAN: 192.168.1.56:5055)
                                │
                                ▼
 [ Open WebUI / Colima Container ] ──(host.docker.internal:5055)──► [ Flask API (Port 5055) ]
                                                                             │
                                                                       (subprocess.Popen)
                                                                             │
                                                                             ▼
                                                                     [ Shell Scripts ]
                                                                             │
                                                                             ▼
                                                                     [ AppleScript ]
                                                                       /         \
                                                                      ▼           ▼
                                                            [ Airfoil ]       [ Google Chrome ]
                                                            (Route Audio)     (Inject JS: "Play All")
                                                                  │               │
                                                                  ▼               ▼
                                                          [ Deck Speakers ] ◄── [ YouTube Audio Stream ]

## The Stack

- **Core Brain:** Mac Mini running Ollama (qwen3:8b / qwen2.5 variants)
- **UI & Chat Environment:** Open WebUI running via Docker/Colima
- **The Translation Layer:** Python Flask (macOS user space)
- **The Puppet Master:** AppleScript & Shell scripting
- **The Hardware & Software Targets:** Rogue Amoeba Airfoil + Google Chrome + YouTube + Raspberry Pi (Shairport Sync)

---

## Core Lessons Learned & Architectural Hacks

### 1. Eliminating Wi-Fi Jitter: The Hardwired Advantage
A massive pain point with consumer outdoor audio (like casting directly from a phone via standard AirPlay) is wireless instability. Walking around a yard with a phone in your pocket routinely causes audio dropouts due to distance, physical obstructions, or hands blocking the device antenna.

"Robot" completely solves this by keeping the heavy-lifting media pipeline entirely on the wire. The Mac Mini is hardwired into the core network switch, and the Raspberry Pi (running Shairport Sync) inside the outdoor deck box is also hardwired back to the switch via Cat6 copper. 

When music plays, the audio packets never travel through the air to reach the speakers. The phone or Open WebUI chat acts strictly as a lightweight, zero-bandwidth remote control interface. You can walk anywhere on the property, move behind brick walls, or turn off your phone entirely, and the audio never stutters or drops.

### 2. Slower Scripts Block iOS Shortcuts (Asynchronous Execution)
Running a macro sequence that launches Chrome, routes physical audio zones, and injects JavaScript takes a few seconds to complete. Apple Shortcuts hates waiting for HTTP responses and will routinely time out and throw an error if an endpoint blocks. 

Pivoting the Flask backend from a standard blocking call to an asynchronous pattern using subprocess.Popen() solved this perfectly. The Flask API immediately replies with a 200 OK "Success!" status to the phone, allowing the iOS widget to close instantly while the Mac Mini continues spinning up the execution scripts in the background.

### 3. The Chrome JavaScript Injection Hack
Bypassing complex OAuth API authentication layers for media platforms is a massive headache for small personal hobby projects. Instead of dealing with API tokens, AppleScript instructs Google Chrome to open a specific, curated public playlist URL and executes a simple query selector to programmatically hit the "Play All" button:

document.querySelector('[aria-label="Play all"]').click()

### 4. Network Topology Matrix (0.0.0.0 vs 127.0.0.1)
I originally bound the Flask API to localhost (127.0.0.1). It worked flawlessly from the Mac itself and from the container environment (via host.docker.internal), but outside devices couldn't discover it. Binding the daemon to 0.0.0.0 opened up the necessary LAN access so physical phone widgets and container triggers could coexist seamlessly using three distinct URL routing patterns:

* Robot Self-Control: http://127.0.0.1:5055
* Open WebUI Container Egress: http://host.docker.internal:5055
* iPhone / Apple Shortcuts / LAN Devices: http://192.168.1.56:5055

### 5. UI Modality: The Hybrid Reality
While controlling everything via a local LLM chat interface is incredibly cool, forcing yourself to open a chat bubble and type text just to skip a track while hanging out on the deck is terrible UX. 

True home automation harmony means using the LLM for complex, context-aware initial staging ("Set up the deck music for a party") and relying on native Apple Shortcuts on the iPhone home screen or Raycast on the Mac for fast, tactical adjustments (Play/Pause, Next Track, All Off).
