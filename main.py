from sim.device_manager import DeviceManager
from backend.server import app
import threading
import requests
import time

def run_simulation():
    print("🚀 Starting SmartEdge simulation...")
    warehouse = DeviceManager(3)
    
    # Start Flask in background
    flask_thread = threading.Thread(
        target=app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False, 'use_reloader': False}
    )
    flask_thread.daemon = True
    flask_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Main simulation loop
    try:
        while True:
            readings = warehouse.poll_all()
            print(f"📦 Collected {len(readings)} sensor readings")
            
            for data in readings:
                try:
                    response = requests.post(
                        "http://localhost:5000/update_inventory",
                        json=data,
                        timeout=3
                    )
                    print(f"📤 Sent: {data['device_id']} = {data['inventory_level']} units")
                except Exception as e:
                    print(f"❌ Failed to send: {e}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped")

if __name__ == '__main__':
    run_simulation()