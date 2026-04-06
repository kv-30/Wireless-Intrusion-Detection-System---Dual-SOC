# fallback_detector.py
def detect_fallback(frames):
    """
    Detect missing or faulty frames
    """
    fallback = [f for f in frames if f.get("rssi") is None]
    return fallback