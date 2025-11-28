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
    <div class="card shadow-lg mb-4">
        <div class="card-header bg-success text-white">
            <h3>About This Project</h3>
        </div>
        <div class="card-body">
            <p><strong>Author:</strong> Alias Saju</p>
            <p><strong>Trigger Source:</strong> Evertz-VUE</p>

            <h5 class="mt-3">Description</h5>
            <p>
            This is a Python-based application designed with modern CI/CD capabilities. It features:
            </p>
            <ul>
                <li>Automated Git Integration: Automatically pulls the latest code and triggers build pipelines.</li>
                <li>Jenkins CI/CD Pipelines: Handles build, test, and deployment automation with detailed logging and error reporting.</li>
                <li>Resource Provisioning and Orchestration via Terraform: Ensures reproducible and managed infrastructure.</li>
                <li>Containerization with Docker: Consistent runtime environment across development and production.</li>
                <li>Deployment to Kubernetes: Provides high availability, horizontal scaling, and orchestration.</li>
                <li>Load Balancing: Efficient distribution of traffic via Kubernetes LoadBalancer.</li>
            </ul>
            <p>More features and updates will be introduced in future releases, enhancing automation, observability, and smart capabilities.</p>

            <h5 class="mt-4">Project Architecture</h5>
            <ul class="list-group">
                <li class="list-group-item">VUE → Python App</li>
                <li class="list-group-item">Python App → Git → Jenkins</li>
                <li class="list-group-item">Jenkins → Docker → Google Artifact Registry</li>
                <li class="list-group-item">Artifact Registry → Kubernetes Cluster → Load Balancer</li>
            </ul>

            <h5 class="mt-4">Tools Used</h5>
            <ul class="list-group">
                <li class="list-group-item">Python</li>
                <li class="list-group-item">Flask</li>
                <li class="list-group-item">YAML</li>
                <li class="list-group-item">Git</li>
                <li class="list-group-item">Jenkins</li>
                <li class="list-group-item">Docker</li>
                <li class="list-group-item">Terraform</li>
                <li class="list-group-item">Google Artifact Registry</li>
                <li class="list-group-item">Kubernetes</li>
                <li class="list-group-item">Bootstrap</li>
            </ul>

            <h5 class="mt-4">Project Flow Diagram</h5>
            <p>Visual representation of the CI/CD and deployment architecture:</p>
            <img src="{{ url_for('static', filename='myappprojectflow.png') }}" class="img-fluid rounded shadow-lg" alt="Project Flow Diagram">

            <a href="/" class="btn btn-primary mt-4">Back to Home</a>
        </div>
    </div>
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



# -------------------- Start Flask --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
