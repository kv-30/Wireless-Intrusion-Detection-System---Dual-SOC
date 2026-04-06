#pragma once

#define LED_PIN 26
#define WIFI_CHANNEL 1
#define BUFFER_SIZE 128 // Circular buffer size

// --------------------
// DUAL-MODE WIFI CONFIGURATION
// --------------------
// AP Mode (always on)
#define WIFI_AP_SSID     "ESP32_Sniffer"
#define WIFI_AP_PASSWORD "12345678"

// STA Mode (connects to external WiFi for MQTT)
// NOTE: For Kali Linux, set these to your WiFi credentials
//       ESP32 will run as AP + STA simultaneously
//       This allows web interface on 192.168.4.1 AND MQTT connectivity
#define ENABLE_STA_MODE 1  // Set to 1 to enable STA client mode
#define WIFI_STA_SSID "Wifi_Name"     // CHANGE THIS to your WiFi network
#define WIFI_STA_PASSWORD "Wifi_Password"  // CHANGE THIS to your WiFi password
#define STA_CONNECTION_TIMEOUT_MS 15000      // Wait 15 seconds for STA connection

// MQTT (accessible after STA connects)
#define MQTT_BROKER "10.10.XX.XX"  // MQTT broker IP on your network
#define MQTT_PORT 1883
#define MQTT_TOPIC "wifi/sniffer"
#define MQTT_CONNECTION_TIMEOUT_MS 10000  // Wait 10 seconds for MQTT connection