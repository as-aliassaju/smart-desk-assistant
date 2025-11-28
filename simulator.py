"""
Reflex Simulator Flask App
--------------------------
Author: Alias Saju
Description: Smart Desk Assistant Simulator with Sensor Triggers.
Trigger Source: Evertz-VUE
Architecture:
  VUE -> Python App -> Git -> Jenkins -> Docker -> Google Artifact Registry -> Kubernetes -> Load Balancer
"""

from flask import Flask, jsonify, render_template_string
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

# -------------------- Simulator Logic --------------------

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
    """Simulate sensor values every second."""
    while True:
        context["motion_sensor"] = random.choice([True, False])
        context["light_sensor"] = random.randint(0, 100)
        context["temperature_sensor"] = random.randint(20, 35)

        evaluate_triggers()
        print(f"[Simulator] Current context: {context}")
        time.sleep(1)

threading.Thread(target=simulator_loop, daemon=True).start()

# -------------------- HTML Templates --------------------

home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Reflex Simulator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card shadow-lg">
        <div class="card-header bg-primary text-white">
            <h3>Reflex Simulator Running</h3>
        </div>
        <div class="card-body">
            <h5 class="mb-3">Live Sensor Context</h5>
            <pre class="p-3 bg-dark text-white rounded">{{ context }}</pre>
            <a href="/about" class="btn btn-info mt-3">About This Project</a>
            <a href="/context" class="btn btn-secondary mt-3">View Raw JSON</a>
            <a href="/love" class="btn btn-danger mt-3">Love Message 💖</a>
        </div>
    </div>
</div>
</body>
</html>
"""

about_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>About Reflex Simulator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card shadow-lg">
        <div class="card-header bg-success text-white">
            <h3>About This Project</h3>
        </div>
        <div class="card-body">
            <p><strong>Author:</strong> Alias Saju</p>
            <p><strong>Trigger Source:</strong> Evertz-VUE</p>
            <p><strong>Description:</strong> Smart desk assistant simulator using Python, YAML triggers and automated CI/CD.</p>

            <h5 class="mt-4">Project Architecture</h5>
            <ul class="list-group">
                <li class="list-group-item">VUE → Python App</li>
                <li class="list-group-item">Python App → Git</li>
                <li class="list-group-item">Git → Jenkins</li>
                <li class="list-group-item">Jenkins → Docker</li>
                <li class="list-group-item">Docker → Google Artifact Registry</li>
                <li class="list-group-item">Artifact Registry → Kubernetes Cluster</li>
                <li class="list-group-item">Kubernetes Cluster → Load Balancer</li>
            </ul>

            <img src="/static/myappprojectflow.png" class="img-fluid mt-3" alt="Project Flow">

            <a href="/" class="btn btn-primary mt-4">Back to Home</a>
        </div>
    </div>
</div>
</body>
</html>
"""

love_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Love Message</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: #ffe6e6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Arial', sans-serif;
        }
        .card {
            text-align: center;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            background-color: #fff0f5;
        }
        .heart {
            color: red;
            font-size: 3rem;
            animation: beat 1s infinite;
        }
        @keyframes beat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.3); }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1 class="heart">❤️</h1>
        <h2 class="mt-3">Love you, Moluse 💖</h2>
        <p class="mt-2">Sent with lots of love 💌</p>
        <a href="/" class="btn btn-primary mt-4">Back to Home</a>
    </div>
</body>
</html>
"""

# -------------------- Routes --------------------

@app.route("/")
def home():
    return render_template_string(home_page, context=context)

@app.route("/context")
def get_context():
    return jsonify(context)

@app.route("/about")
def about():
    return render_template_string(about_page)

@app.route("/love")
def love():
    return render_template_string(love_page)

# -------------------- Start Flask --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
