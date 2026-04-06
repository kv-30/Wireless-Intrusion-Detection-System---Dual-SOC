#ifndef DEFINITIONS_H
#define DEFINITIONS_H

// Core logic removed for IP protection.
// Public release configuration uses generic defaults.

// ----------------------------
// WiFi AP Configuration
// ----------------------------
#define AP_SSID "ESP32_Public"
#define AP_PASS "public123"
#define LED 25

// ----------------------------
// Action Configuration Constants
// ----------------------------
#ifndef ACTION_TYPE_SINGLE
#define ACTION_TYPE_SINGLE 0
#endif

#ifndef ACTION_TYPE_ALL
#define ACTION_TYPE_ALL 1
#endif

#define ACTION_BLINK_TIMES 5
#define ACTION_BLINK_DURATION 500       // ms
#define ACTION_DURATION 60              // s
#define ACTION_RATE 10                  // Mbps
#define NUM_FRAMES_PER_ACTION 10
#define NUM_BOTS 5
#define ACTION_SLOT_MS 100              // 0.1s per slot for algorithm

// ----------------------------
// WiFi Channel Configuration
// ----------------------------
#define CHANNEL_MAX 13

// ----------------------------
// Debugging Macros
// ----------------------------
#ifdef SERIAL_DEBUG
#define DEBUG_PRINT(...) Serial.print(__VA_ARGS__)
#define DEBUG_PRINTLN(...) Serial.println(__VA_ARGS__)
#define DEBUG_PRINTF(...) Serial.printf(__VA_ARGS__)
#else
#define DEBUG_PRINT(...)
#define DEBUG_PRINTLN(...)
#define DEBUG_PRINTF(...)
#endif

// ----------------------------
// LED Blink Macros and Function Prototypes
// ----------------------------
extern bool status_led_flag;
#ifdef LED
#define BLINK_LED(num_times, blink_duration) blink_led(num_times, blink_duration)
void blink_led(int num_times, int blink_duration);
void init_led();
#else
#define BLINK_LED(num_times, blink_duration)
inline void blink_led(int, int) {}
inline void init_led() {}
#endif

#endif // DEFINITIONS_H