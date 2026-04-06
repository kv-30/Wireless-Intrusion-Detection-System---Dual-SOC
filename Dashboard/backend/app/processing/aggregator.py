# aggregator.py
def aggregate_frames(silver_data):
    """
    Aggregate Silver layer frames into summary for ML
    """
    aggregated = {}
    # Example: calculate avg RSSI per MAC
    rssi_values = [f['rssi'] for f in silver_data]
    aggregated["avg_rssi"] = sum(rssi_values)/len(rssi_values) if rssi_values else 0
    return aggregated