#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "web_interface.h"
#include "globals.h"
#include "config.h"
#include "wifi_sniffer.h"
#include "streamer.h"

// --------------------
// WiFi + MQTT state tracking
// --------------------
unsigned long lastMqttAttempt = 0;
const unsigned long MQTT_RETRY_INTERVAL_MS = 5000;  // Retry every 5 seconds
const unsigned long MQTT_BROKER_UNREACHABLE_INTERVAL_MS = 15000;  // If unreachable, wait 15 seconds
bool staConnected = false;
bool lastIPEventPrinted = false;  // Prevent duplicate IP prints
unsigned long staConnectStart = 0;
unsigned long lastWifiCheck = 0;
const unsigned long WIFI_CHECK_INTERVAL = 10000;  // Check WiFi status every 10 seconds
int lastMqttErrorCode = 0;  // Track last error to adjust retry strategy

// --------------------
// WiFi event handler
// --------------------
void WiFiStationEvent(arduino_event_t *event) {
    switch(event->event_id) {
        case ARDUINO_EVENT_WIFI_STA_START:
            Serial.println("[WiFi] STA mode started, attempting to connect...");
            break;
        case ARDUINO_EVENT_WIFI_STA_CONNECTED:
            Serial.println("[WiFi] Connected to WiFi network");
            staConnected = true;
            break;
        case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
            Serial.println("[WiFi] Disconnected from WiFi network");
            staConnected = false;
            lastIPEventPrinted = false;  // Reset for next IP event
            if (mqttClient.connected()) {
                mqttClient.disconnect();
                Serial.println("[MQTT] Disconnected due to WiFi loss");
            }
            break;
        case ARDUINO_EVENT_WIFI_STA_GOT_IP:
            if (!lastIPEventPrinted) {  // Only print once per connection
                Serial.print("[WiFi] Got IP address: ");
                Serial.println(WiFi.localIP());
                Serial.println("[WiFi] ✓ WiFi connection established - MQTT connection will now be attempted");
                lastIPEventPrinted = true;
            }
            staConnected = true;  // Mark as fully connected when IP is obtained
            break;
        default:
            break;
    }
}

// --------------------
// MQTT reconnect helper (non-blocking, requires WiFi)
// --------------------
void mqtt_reconnect() {
    if (mqttClient.connected()) return;
    if (!staConnected) return;  // Wait for WiFi connection first
    if (WiFi.status() != WL_CONNECTED) return;  // Verify WiFi still connected
    
    unsigned long now = millis();
    
    // Adapt retry interval based on last error
    unsigned long retryInterval = MQTT_RETRY_INTERVAL_MS;
    if (lastMqttErrorCode == -2 || lastMqttErrorCode == -1) {
        // Broker unreachable or connection failed - wait longer
        retryInterval = MQTT_BROKER_UNREACHABLE_INTERVAL_MS;
    }
    
    if (now - lastMqttAttempt < retryInterval) return;  // Not time to retry yet
    
    lastMqttAttempt = now;
    
    char clientId[32];
    snprintf(clientId, sizeof(clientId), "ESP32Sniffer-%u", (unsigned int)(millis() & 0xFFFF));
    
    // Minimal logging to avoid buffer overflow
    if (mqttClient.connect(clientId)) {
        Serial.println("[MQTT] ✓ Connected successfully!");
        lastMqttErrorCode = 0;  // Reset error code on success
    } else {
        int state = mqttClient.state();
        lastMqttErrorCode = state;
        
        // Only log critical errors, not every retry
        static unsigned long lastMqttLogTime = 0;
        if(now - lastMqttLogTime > 30000) {  // Log errors only every 30 seconds
            lastMqttLogTime = now;
            Serial.printf("[MQTT] Connection failed (code: %d). Verify broker at %s:%d is running\n", state, MQTT_BROKER, MQTT_PORT);
        }
    }
}

// --------------------
// Setup
// --------------------
void setup() {
    Serial.begin(115200);
    delay(1000);  // Wait 1 second for USB to stabilize
    Serial.flush();  // Clear any garbage from bootloader
    Serial.println("\n\n[SETUP] ESP32 WiFi Sniffer starting...");
    
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH);  // LED on to indicate power

    // --------------------
    // Configure WiFi with dual mode (AP + STA)
    // --------------------
#if ENABLE_STA_MODE
    WiFi.mode(WIFI_MODE_APSTA);  // Both AP and STA (client) mode
    Serial.println("[WiFi] Dual mode enabled (AP + STA)");
    
    // Improve WiFi stability for dual-mode
    WiFi.setSleep(WIFI_PS_NONE);  // Disable WiFi power saving to stabilize dual-mode
    WiFi.setTxPower(WIFI_POWER_19_5dBm);  // Use consistent TX power
    
    // Setup AP (for web interface)
    WiFi.softAP(WIFI_AP_SSID, WIFI_AP_PASSWORD, WIFI_CHANNEL);
    Serial.print("[WiFi] AP started at IP: ");
    Serial.println(WiFi.softAPIP());
    Serial.printf("[WiFi] SSID: %s\n", WIFI_AP_SSID);
    
    // Setup WiFi event listener
    WiFi.onEvent(WiFiStationEvent);
    
    // Connect to external WiFi (STA mode)
    Serial.printf("[WiFi] Connecting to STA: %s...\n", WIFI_STA_SSID);
    WiFi.begin(WIFI_STA_SSID, WIFI_STA_PASSWORD);
    staConnectStart = millis();
#else
    // AP-only mode (no MQTT)
    WiFi.mode(WIFI_MODE_AP);
    WiFi.softAP(WIFI_AP_SSID, WIFI_AP_PASSWORD);
    Serial.print("[WiFi] AP-only mode at IP: ");
    Serial.println(WiFi.softAPIP());
    Serial.println("[MQTT] STA mode disabled - MQTT will not work");
#endif

    // --------------------
    // Initialize MQTT
    // --------------------
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    Serial.printf("[MQTT] Broker set to %s:%d\n", MQTT_BROKER, MQTT_PORT);

    // --------------------
    // Initialize Web Interface
    // --------------------
    init_web_interface();

    // --------------------
    // Initialize sniffer (idle by default)
    // --------------------
    init_sniffer();
    
    Serial.println("[SETUP] Initialization complete\n");
}

// --------------------
// Loop
// --------------------
unsigned long lastStream = 0;
const unsigned long STREAM_INTERVAL_MS = 500;  // 500ms interval

void loop() {
    // Handle web clients
    web_interface_handle_client();

#if ENABLE_STA_MODE
    // WiFi status tracking (minimal logging during operation)
    wl_status_t currentWifiStatus = WiFi.status();
    
    // Check STA connection status (non-blocking) - print less frequently to avoid spam
    static unsigned long lastWifiStatus = 0;
    if (!staConnected && (millis() - staConnectStart < STA_CONNECTION_TIMEOUT_MS)) {
        // Print status every 5 seconds instead of 2
        if (millis() - lastWifiStatus > 5000) {
            Serial.printf("[WiFi] Connecting... (%lums elapsed, status=%d)\n", millis() - staConnectStart, currentWifiStatus);
            lastWifiStatus = millis();
        }
    }
    
    // Periodically verify WiFi connection is still active
    if (millis() - lastWifiCheck > WIFI_CHECK_INTERVAL) {
        lastWifiCheck = millis();
        if (currentWifiStatus != WL_CONNECTED && staConnected) {
            // WiFi was connected but now disconnected - reconnect
            Serial.println("[WiFi] Connection lost, attempting to reconnect...");
            staConnected = false;
            WiFi.reconnect();
            staConnectStart = millis();
        }
    }
    
    // Ensure MQTT is connected (only if WiFi is connected)
    if (staConnected && currentWifiStatus == WL_CONNECTED) {
        mqtt_reconnect();
        mqttClient.loop();
    }
#endif

    // Stream frames only if sniffing is active
    if (sniffing_active) {
        unsigned long now = millis();
        if (now - lastStream >= STREAM_INTERVAL_MS) {
            stream_frames_mqtt();
            lastStream = now;
        }
    }
    
    // Print periodic system status (every 30 seconds)
    print_system_status();
    
    // Keep MQTT alive during sniffing by calling loop frequently
    if (mqttClient.connected()) {
        mqttClient.loop();
    }
}