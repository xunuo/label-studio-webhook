# main.py
import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_payload(payload: dict):
    logger.info("Handling payload: %s", payload)
    # 你的业务逻辑……
    return {"status": "processed", "size": len(payload)}

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    logger.info("▶ Webhook payload: %s", payload)
    result = process_payload(payload)
    return jsonify({"status": "ok", "result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
