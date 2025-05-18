import random
import time

class VirtualSensor:
    def __init__(self, device_id, start_level=100):
        self.device_id = device_id
        self.inventory_level = start_level
        self.last_restock = time.time()

    def read_inventory(self):
        drop = random.uniform(0.5, 2.0)
        
        # 5% chance of big drop
        if random.random() < 0.05:
            drop += random.uniform(5, 15)
            
        self.inventory_level = max(self.inventory_level - drop, 0)
        
        return {
            "device_id": self.device_id,
            "timestamp": time.time(),
            "inventory_level": round(self.inventory_level, 2)
        }
    
    def restock(self):
        self.inventory_level = 100
        self.last_restock = time.time()