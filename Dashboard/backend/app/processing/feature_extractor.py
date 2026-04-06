# feature_extractor.py
def extract_features(frames):
    """
    Convert raw frames into feature dicts for Silver layer
    """
    features_list = []
    for frame in frames:
        features = {
            "mac": frame.get("mac"),
            "rssi": frame.get("rssi"),
            "entropy": frame.get("entropy", 0),
            "timestamp": frame.get("timestamp")
        }
        features_list.append(features)
    return features_list