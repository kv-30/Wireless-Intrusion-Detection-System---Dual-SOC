#include "globals.h"

CircularBuffer frameBuffer(BUFFER_SIZE);

WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Sniffer state
bool sniffing_active = false;  // false initially