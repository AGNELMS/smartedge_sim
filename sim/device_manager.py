from .virtual_sensor import VirtualSensor
import time

class DeviceManager:
    """Manages multiple virtual sensors"""
    def __init__(self, num_devices=3):
        self.devices = [VirtualSensor(f"Sensor-{i+1}") for i in range(num_devices)]

    def poll_all(self):
        """Get readings from all sensors"""
        return [device.read_inventory() for device in self.devices]