from flask import Flask
import os
import yaml
import subprocess
import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(BASE_DIR, "context.yaml")

@app.route("/updateTextFile", methods=["POST"])
def update_count():

    print("New VUE event received")

    # Load existing YAML
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE) as f:
            data = yaml.safe_load(f)
    else:
        data = {"context": {"event_count": 0}}

    # Increment count
    data["context"]["event_count"] += 1

    # Save file
    with open(CONTEXT_FILE, "w") as f:
        yaml.dump(data, f)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        subprocess.run(["git", "add", "context.yaml"], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Event count updated to {data['context']['event_count']} at {timestamp}"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("Git push successful")

    except Exception as e:
        print("Git push failed:", e)

    return {
        "status": "OK",
        "event_count": data["context"]["event_count"]
    }, 200


app.run(host="192.168.56.1", port=5000)