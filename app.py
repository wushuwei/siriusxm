# app.py
import os
import threading
from flask import Flask, jsonify
from sxm import SXMClient, SXMProxy

app = Flask(__name__)

# Read credentials from environment variables
username = os.environ.get("SIRIUSXM_USER")
password = os.environ.get("SIRIUSXM_PASS")

if not username or not password:
    raise RuntimeError("Please set SIRIUSXM_USER and SIRIUSXM_PASS environment variables")

# Login with SiriusXM credentials
client = SXMClient(username, password)

# Start proxy in background
proxy = SXMProxy(client)
threading.Thread(target=lambda: proxy.start(port=8888), daemon=True).start()

@app.route("/channels")
def channels():
    return jsonify([
        {"id": ch.id, "name": ch.name}
        for ch in client.channels
    ])

@app.route("/stream/<channel_id>")
def stream(channel_id):
    ch = client.get_channel(channel_id)
    return jsonify({
        "id": ch.id,
        "name": ch.name,
        "url": f"http://127.0.0.1:8888/{ch.id}.m3u8"
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)