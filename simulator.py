import yaml
import time
import random

# Load YAML files
with open("context.yaml") as f:
    context = yaml.safe_load(f)["context"]

with open("triggers.yaml") as f:
    triggers = yaml.safe_load(f)["triggers"]

def evaluate_triggers():
    for trigger_name, trigger in triggers.items():
        condition = trigger["condition"]
        # Evaluate condition using context variables
        if eval(condition, {}, context):
            exec(trigger["action"], {}, context)

print("=== Smart Desk Assistant Simulator ===")

for i in range(5):  # Simulate 5 cycles
    # Randomly change sensor values
    context["motion_sensor"] = random.choice([True, False])
    context["light_sensor"] = random.randint(0, 100)
    context["temperature_sensor"] = random.randint(20, 35)

    print(f"\nCycle {i+1} - Sensor Values: {context}")
    evaluate_triggers()
    time.sleep(1)
