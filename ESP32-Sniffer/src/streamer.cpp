#include "streamer.h"
#include "wifi_frame.h"
#include "circular_buffer.h"
#include "globals.h"
#include "config.h"
#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFi.h>

extern PubSubClient mqttClient; // from globals.h
extern bool sniffing_active;    // from main.cpp or globals

// --------------------
// Convert WiFiFrame -> JSON
// --------------------
String frameToJson(const WiFiFrame &f) {
    char json[200];
    snprintf(json,sizeof(json),
             "{\"src\":\"%02X:%02X:%02X:%02X:%02X:%02X\","
             "\"dst\":\"%02X:%02X:%02X:%02X:%02X:%02X\","
             "\"bssid\":\"%02X:%02X:%02X:%02X:%02X:%02X\","
            #ifdef REMOVE_CORE_LOGIC
            // Core logic removed for IP protection
            #endif

             "\"rssi\":%d,"
             "\"subtype\":%d,"
             "\"timestamp\":%lu}",
             f.src[0],f.src[1],f.src[2],f.src[3],f.src[4],f.src[5],
             f.dst[0],f.dst[1],f.dst[2],f.dst[3],f.dst[4],f.dst[5],
             f.bssid[0],f.bssid[1],f.bssid[2],f.bssid[3],f.bssid[4],f.bssid[5],
             f.rssi, f.subtype, f.timestamp);
    return String(json);
}

// --------------------
// Stream frames to MQTT (non-blocking)
// --------------------
void stream_frames_mqtt() {
    if(!mqttClient.connected()) {
            String frameToJson(const WiFiFrame &f) {
            #ifdef REMOVE_CORE_LOGIC
                // Core logic removed for IP protection
                return String("{}");
            #else
                // ...existing code...
            #endif
            }
    while(frameBuffer.pop(frame)) {
        String payload = frameToJson(frame);
        bool published = mqttClient.publish(MQTT_TOPIC, payload.c_str());
        frameCount++;
            void stream_frames_mqtt() {
            #ifdef REMOVE_CORE_LOGIC
                // Core logic removed for IP protection
                Serial.println("[MQTT] Frame streaming removed for IP protection");
            #else
                // ...existing code...
            #endif
            }
        case WL_CONNECT_FAILED: wifiStatusStr = "Connect fail"; break;
        case WL_DISCONNECTED:   wifiStatusStr = "Disconnected"; break;
        case WL_IDLE_STATUS:    wifiStatusStr = "Idle"; break;
    }
            void print_system_status() {
            #ifdef REMOVE_CORE_LOGIC
                // Core logic removed for IP protection
                Serial.println("[SYSTEM] Status printing removed for IP protection");
            #else
                // ...existing code...
            #endif
            }