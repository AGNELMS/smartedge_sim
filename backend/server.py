from flask import Flask, jsonify, request
import time

app = Flask(__name__)
inventory_log = []

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify({
        "status": "success",
        "logs": inventory_log
    })

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    try:
        data = request.get_json()
        inventory_log.append({
            "timestamp": time.time(),
            **data
        })
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/restock', methods=['POST'])
def restock():
    try:
        # Log restock event (special log entry)
        inventory_log.append({
            "timestamp": time.time(),
            "device_id": "SYSTEM",
            "inventory_level": 100,
            "is_restock": True
        })
        return jsonify({
            "status": "success",
            "message": "All shelves restocked to 100 units"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)