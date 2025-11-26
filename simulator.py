from flask import Flask, jsonify
import yaml
import random
import threading
import time

app = Flask(__name__)

# Load context and triggers
with open("context.yaml") as f:
    context = yaml.safe_load(f)["context"]

with open("triggers.yaml") as f:
    triggers = yaml.safe_load(f)["triggers"]

def evaluate_triggers():
    """Evaluate triggers based on the current context."""
    for trigger_name, trigger in triggers.items():
        condition = trigger.get("condition")
        action = trigger.get("action")
        try:
            if eval(condition, {}, context):
                exec(action, {}, context)
        except Exception as e:
            print(f"Error in trigger {trigger_name}: {e}")

def simulator_loop():
    """Simulate sensor updates continuously."""
    while True:
        # Randomly change sensor values
        context["motion_sensor"] = random.choice([True, False])
        context["light_sensor"] = random.randint(0, 100)
        context["temperature_sensor"] = random.randint(20, 35)

        # Evaluate triggers
        evaluate_triggers()

        # Print current context
        print(f"[Simulator] Current context: {context}")
        time.sleep(1)

# Start the simulator in a background thread
threading.Thread(target=simulator_loop, daemon=True).start()

@app.route("/")
def home():
    return jsonify({"status": "Reflex Simulator Running", "context": context})

@app.route("/context")
def get_context():
    return jsonify(context)

if __name__ == "__main__":
    # Flask runs on 0.0.0.0 so Kubernetes can access it
    app.run(host="0.0.0.0", port=5000)

