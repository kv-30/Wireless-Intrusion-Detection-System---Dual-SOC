#pragma once
#include <cstdint>

struct WiFiFrame {
    uint64_t timestamp;
    uint8_t src[6];
    uint8_t dst[6];
    uint8_t bssid[6];
    int rssi;
    uint8_t subtype;
};