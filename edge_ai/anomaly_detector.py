class AnomalyDetector:
    """Checks for unusual inventory drops"""
    def __init__(self, threshold=5.0):
        self.threshold = threshold

    def check_anomaly(self, current, previous):
        drop = previous - current
        if drop > self.threshold:
            return True, f"🚨 Alert: Drop of {drop:.2f} units!"
        return False, ""