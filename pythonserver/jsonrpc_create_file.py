from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Existing Flask server endpoint
TARGET_URL = "http://127.0.0.1:5000/create-file"  # your original Flask app

@app.route("/jsonrpc", methods=["POST"])
def jsonrpc_middleware():
    try:
        # -----------------------------
        # Parse incoming JSON-RPC payload from Magnum
        # -----------------------------
        try:
            rpc_data = request.get_json(force=True)
        except Exception:
            raw = request.get_data(as_text=True)
            rpc_data = json.loads(raw)

        print("Received JSON-RPC payload from Magnum:", rpc_data)

        rpc_id = rpc_data.get("id", None)
        method = rpc_data.get("method", "")
        params = rpc_data.get("params", {})

        if method != "createFile":
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": rpc_id})

        # -----------------------------
        # Forward to the original Flask server via HTTP POST
        # -----------------------------
        post_data = {
            "text": params.get("text", "No message"),
            "button": params.get("button", "unknown_button")
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(TARGET_URL, json=post_data, headers=headers, timeout=5)

        # -----------------------------
        # Prepare JSON-RPC response
        # -----------------------------
        if response.status_code == 200:
            return jsonify({
                "jsonrpc": "2.0",
                "result": response.json(),  # pass through the original Flask response
                "id": rpc_id
            })
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": f"Upstream server returned {response.status_code}"},
                "id": rpc_id
            })

    except Exception as e:
        print("Exception in middleware:", e)
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None})


if __name__ == "__main__":
    app.run(host="192.168.56.1", port=6000, debug=True)
