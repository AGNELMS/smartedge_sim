from flask import Flask, jsonify, request
import time
from threading import Lock

app = Flask(__name__)
inventory_log = []
log_lock = Lock()

@app.route('/get_logs', methods=['GET'])
def get_logs():
    with log_lock:
        return jsonify({
            "status": "success",
            "logs": inventory_log
        })

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    try:
        data = request.get_json()
        with log_lock:
            inventory_log.append({
                "timestamp": time.time(),
                **data
            })
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)