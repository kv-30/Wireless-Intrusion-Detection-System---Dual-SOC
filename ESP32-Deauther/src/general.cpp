#include <Arduino.h>
#include "definitions.h"

#ifdef LED
// ----------------------------
// Global LED flag
// ----------------------------
bool status_led_flag = false;

// ----------------------------
// Initialize LED at boot
// ----------------------------
void init_led() {
    pinMode(LED, OUTPUT);
    digitalWrite(LED, HIGH);  // LED ON at boot
}

// ----------------------------
// Blink LED (simple blocking version)
// ----------------------------
void blink_led(int num_times, int blink_duration) {
    for (int i = 0; i < num_times; i++) {
        digitalWrite(LED, LOW);
        delay(blink_duration / 2);
        digitalWrite(LED, HIGH);
        delay(blink_duration / 2);
    }
}

#else
// Dummy functions if LED not defined
void init_led() {}
void blink_led(int, int) {}
#endif