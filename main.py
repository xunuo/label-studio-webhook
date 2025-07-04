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



from handler import process_payload  # 或者你的业务逻辑模块

# 配置 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # 1. 读取 Referer
    referer = request.headers.get("Referer")
    logger.info("▶ Request Referer: %s", referer)

    # 2. 读取并校验 JSON payload
    payload = request.get_json(force=True)
    if not payload:
        logger.warning("▶ 无效 JSON 请求，Referer: %s", referer)
        return jsonify({"error": "Invalid JSON"}), 400

    # 3. 打印 payload
    logger.info("▶ Webhook payload: %s", payload)

    # 4. 调用你的处理逻辑
    try:
        result = process_payload(payload)
    except Exception as e:
        logger.exception("▶ 处理 payload 时出错，Referer: %s", referer)
        return jsonify({"error": str(e)}), 500

    # 5. 返回
    return jsonify({"status": "ok", "result": result})
