#ifndef WEB_INTERFACE_H
#define WEB_INTERFACE_H

#include <Arduino.h>
#include <WiFi.h>
#include "definitions.h"

// Core logic removed for IP protection.
// Only the public web interface API is preserved.

extern bool operation_in_progress;          // Flag: is action running

void start_web_interface();              // Initialize the web server
void web_interface_handle_client();      // Handle client requests

#endif 