import os
import logging
from flask import Flask, request, jsonify
from handler import process_payload

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 简易内存队列，最多保留最新 20 条
received = []

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    # 缓存到内存
    received.insert(0, payload)
    if len(received) > 20:
        received.pop()

    logger.info("▶ Webhook payload cached")
    # 继续调用你的逻辑
    result = process_payload(payload)
    return jsonify({"status": "ok", "result": result})

@app.route("/debug", methods=["GET"])
def debug():
    """
    访问这个接口就能看到最近 20 条完整的 payload JSON
    """
    return jsonify(received)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))


