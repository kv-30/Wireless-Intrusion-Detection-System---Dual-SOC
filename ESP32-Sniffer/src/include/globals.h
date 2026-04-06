#pragma once
#include "circular_buffer.h"
#include "config.h"
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <WiFi.h>

// Frame buffer for captured Wi-Fi frames
extern CircularBuffer frameBuffer;

// MQTT client
extern WiFiClient espClient;
extern PubSubClient mqttClient;

// LED pin
#define LED_PIN 26

// Sniffer state (shared across web interface and main)
extern bool sniffing_active;

// WiFi state
extern bool staConnected;  // Indicates if STA (external WiFi) is connected

inline String macToStr(const uint8_t* mac) {
    char buf[18];
    snprintf(buf, sizeof(buf), "%02X:%02X:%02X:%02X:%02X:%02X",
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    return String(buf);
}