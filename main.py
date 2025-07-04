from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


# 配置 logging，把 INFO 级别以上的日志都输出到 stdout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(force=True, silent=False)
    if not payload:
        logger.warning("收到无效 JSON")
        return jsonify({"error": "Invalid JSON"}), 400

    # 这一行会把完整的 JSON payload 输出到 stdout
    logger.info("▶ Webhook payload: %s", payload)

    try:
        result = process_payload(payload)
    except Exception as e:
        logger.exception("处理 payload 时出错")
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok", "result": result})
    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
