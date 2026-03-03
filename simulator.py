from flask import Flask, jsonify, render_template_string, url_for
import yaml
import os

app = Flask(__name__)

# -------- Load Context --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(BASE_DIR, "context.yaml")

def load_context():
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE) as f:
            return yaml.safe_load(f)["context"]
    else:
        return {"event_count": 0}

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
            <h5 class="mb-3">Live Context Data</h5>
            <pre class="p-3 bg-dark text-white rounded">{{ context }}</pre>
            <a href="/about" class="btn btn-info mt-3">About This Project</a>
            <a href="/counter" class="btn btn-success mt-3">View Counter</a>
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
    <title>VUE->Python CI/CD Project</title>
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
            This is a Python-based application designed with modern CI/CD capabilities.
            It integrates Git, Jenkins, Docker, Google Artifact Registry, and Kubernetes
            for automated build and deployment workflows.
            </p>

            <h5 class="mt-4">Project Architecture</h5>
            <ul class="list-group">
                <li class="list-group-item">VUE → Python App</li>
                <li class="list-group-item">Python App → Git → Jenkins</li>
                <li class="list-group-item">Jenkins → Docker → Google Artifact Registry</li>
                <li class="list-group-item">Artifact Registry → Kubernetes → Load Balancer</li>
            </ul>

            <h5 class="mt-4">Workflow Diagram</h5>
            <div class="text-center mt-3">
                <img src="{{ url_for('static', filename='myappprojectflow.png') }}"
                     class="img-fluid rounded shadow"
                     alt="Project Workflow Diagram">
            </div>

            <a href="/" class="btn btn-primary mt-4">Back to Home</a>
        </div>
    </div>
</div>
</body>
</html>
"""

counter_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Counter</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card shadow-lg text-center">
        <div class="card-header bg-dark text-white">
            <h3>Current Counter Value</h3>
        </div>
        <div class="card-body">
            <h1 class="display-3">{{ context['event_count'] }}</h1>
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
    return render_template_string(home_page, context=load_context())

@app.route("/about")
def about():
    return render_template_string(about_page)

@app.route("/counter")
def counter():
    return render_template_string(counter_page, context=load_context())

@app.route("/context")
def get_context():
    return jsonify(load_context())

# -------------------- Start Flask --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)