#pragma once
#include <Arduino.h>

// Initialize sniffer (callback registered but idle)
void init_sniffer();

// Start sniffing on a specific channel
void start_sniffer(uint8_t channel);

// Stop sniffing
void stop_sniffer();