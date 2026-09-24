import os
import socket
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "v1")
COLOR = os.environ.get("APP_COLOR", "#2196F3")
APP_NAME = os.environ.get("APP_NAME", "Sample App")
HOSTNAME = socket.gethostname()
START_TIME = time.time()


@app.route("/")
def index():
    return render_template(
        "index.html",
        version=VERSION,
        color=COLOR,
        app_name=APP_NAME,
        hostname=HOSTNAME,
    )


@app.route("/api/info")
def info():
    return jsonify(
        {
            "version": VERSION,
            "app_name": APP_NAME,
            "hostname": HOSTNAME,
            "uptime_seconds": round(time.time() - START_TIME, 2),
            "headers": dict(request.headers),
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": VERSION})


if __name__ == "__main__":
    print(f"Starting {APP_NAME} {VERSION} on port 8080")
    app.run(host="0.0.0.0", port=8080)
