#include <WiFi.h>
#include <esp_wifi.h>
#include "types.h"
#include "web_interface.h"
#include "deauth.h"
#include "definitions.h"

int curr_channel = 1;

void setup() {
#ifdef SERIAL_DEBUG
    Serial.begin(115200);
#endif

#ifdef LED
    init_led();
#endif

    WiFi.mode(WIFI_MODE_AP);
    WiFi.softAP(AP_SSID, AP_PASS);

    start_web_interface();
}

void loop() {
    web_interface_handle_client();

    if (operation_in_progress) {
        update_operation_status();

        if (status_led_flag) {
            status_led_flag = false;
            BLINK_LED(ACTION_BLINK_TIMES, ACTION_BLINK_DURATION);
        }
    }
    else {
        // Placeholder idle behavior for public release.
        delay(100);
    }
}