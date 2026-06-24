app = Flask(__name__)

SCRIPTS = {
    "backyard": "/Users/robot/robot-actions/airfoil/backyard-chrome-on.sh",
    "backyard_living_room": "/Users/robot/robot-actions/airfoil/backyard-living-room-on.sh",
    "backyard_off": "/Users/robot/robot-actions/airfoil/backyard-off.sh",
    "all_off": "/Users/robot/robot-actions/airfoil/all-off.sh",
    "play_deck_music": "/Users/robot/robot-actions/airfoil/play-deck-music.sh",
    "play_pause_music": "/Users/robot/robot-actions/airfoil/play-pause-music.sh",
    "next_track": "/Users/robot/robot-actions/airfoil/next-track.sh",
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/speakers", methods=["GET"])
def speakers():
    result = subprocess.run(
        ["osascript", "-e", 'tell application "Airfoil" to get name of every speaker'],
        capture_output=True,
        text=True,
        timeout=10
    )

    return jsonify({
        "returncode": result.returncode,
        "speakers": result.stdout.strip(),
        "stderr": result.stderr.strip()
    })

@app.route("/airfoil/<action>", methods=["POST"])
def airfoil(action):
    if action not in SCRIPTS:
        return jsonify({"error": "Unknown action"}), 404

    result = subprocess.run(
        [SCRIPTS[action]],
        capture_output=True,
        text=True,
        timeout=15
    )

    return jsonify({
        "action": action,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    })

@app.route("/music/play_deck", methods=["POST"])
def play_deck():
    subprocess.Popen(
        [SCRIPTS["play_deck_music"]],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return jsonify({
        "action": "play_deck_music",
        "status": "started"
    })

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

@app.route("/music/next", methods=["POST"])
def next_track():
    subprocess.Popen(
        [SCRIPTS["next_track"]],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return jsonify({
        "action": "next_track",
        "status": "started"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)
