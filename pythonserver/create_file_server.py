from flask import Flask, request
import os
import datetime
import subprocess

app = Flask(__name__)

@app.route("/create-file", methods=["POST"])
def log_event():
    print("\n---------------------------")
    print("NEW REQUEST RECEIVED")
    print("---------------------------")

    # 🔥 Never parse JSON automatically – do it silently
    #body = request.get_data(as_text=True)
    #print("Raw body:", body)

    # Folder where log file exists
    print("FUNCTION EXECUTED!")
    folder = r"C:\Users\aliassaju\smart_desk_assistant"
    os.makedirs(folder, exist_ok=True)

    log_file = os.path.join(folder, "VUE_DATA.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append only timestamp
    with open(log_file, "a") as f:
        f.write(f"[EVENT RECEIVED] {timestamp}\n")

    print(f"Logged timestamp → {log_file}")

    # ----------------------------
# 🔥 AUTO GIT COMMIT + PUSH
# ----------------------------
    try:
        # Change working directory to repo
        os.chdir(folder)

        # Add file
        subprocess.run(["git", "add", "VUE_DATA.txt"], check=True)

        # Commit with a clear message
        commit_message = f"Event created from VUE: {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push to origin
        subprocess.run(["git", "push"], check=True)

        print(f"Git push successful! Commit message: '{commit_message}'")

    except Exception as e:
        print("Git operation failed:", e)

    # ALWAYS return 200 (VUE may send trash — ignore it)
    return {"status": "OK", "timestamp": timestamp}, 200

# IMPORTANT: Turn off Flask JSON parse failures
app.config['JSON_AS_ASCII'] = False

# 🔥 Disable all strict request parsing
app.url_map.strict_slashes = False

app.run(host="192.168.56.1", port=5000)
