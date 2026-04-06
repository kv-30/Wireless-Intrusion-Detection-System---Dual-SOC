# app/db/test_bronze_insert.py
from app.db.bronze import write_bronze

frames = [
    {"src": "aa:bb:cc:dd:ee:ff", "dst": "11:22:33:44:55:66", "subtype": "deauth", "rssi": -50},
    {"src": "aa:bb:cc:dd:ee:11", "dst": "11:22:33:44:55:77", "subtype": "data", "rssi": -60},
    {"src": "aa:bb:cc:dd:ee:22", "dst": "11:22:33:44:55:88", "subtype": "data", "rssi": -70},
]

write_bronze(frames)
print(f"Inserted {len(frames)} sample frames into Bronze bucket")