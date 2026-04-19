from flask import Flask
import os
import yaml
import subprocess
import datetime

app = Flask(__name__)

# Move one level up from pythonserver → smart_desk_assistant
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CONTEXT_FILE = os.path.join(BASE_DIR, "context.yaml")


@app.route("/updateTextFile", methods=["GET","POST"])
def update_count():

    print("New VUE event received")
    print("Running Git from:", BASE_DIR)
    print("Context file:", CONTEXT_FILE)

    # Load existing YAML (must exist)
    if not os.path.exists(CONTEXT_FILE):
        return {"status": "ERROR", "message": "context.yaml not found"}, 500

    with open(CONTEXT_FILE, "r") as f:
        data = yaml.safe_load(f)

    # Increment event count
    data["context"]["event_count"] += 1

    # Save file
    with open(CONTEXT_FILE, "w") as f:
        yaml.dump(data, f)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        subprocess.run(["git", "add", "context.yaml"], cwd=BASE_DIR, check=True)

        subprocess.run(
            [
                "git", "commit",
                "-m",
                f"Event count updated to {data['context']['event_count']} at {timestamp}"
            ],
            cwd=BASE_DIR,
            check=True
        )

        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)

        print("Git push successful")

    except subprocess.CalledProcessError as e:
        print("Git push failed:", e)
        return {"status": "ERROR", "message": str(e)}, 500

    return {
        "status": "OK",
        "event_count": data["context"]["event_count"]
    }, 200


if __name__ == "__main__":
    app.run(host="192.168.56.1", port=5000)