# ESP32-Sniffer

A Wi-Fi sniffer and MQTT streaming tool for ESP32, featuring dual-mode Wi-Fi (AP + STA), web interface, and real-time frame capture. Built with PlatformIO and Arduino framework.

---

## Features
- Captures Wi-Fi management frames in real time
- Streams captured frames to an MQTT broker (for integration with tools like Wireshark, custom dashboards, etc.)
- Web interface for live monitoring and control (accessible at `192.168.4.1`)
- Dual-mode Wi-Fi: ESP32 acts as both AP (for web UI) and STA (for MQTT)
- Circular buffer for efficient frame storage
- Configurable via `config.h`

---

## Hardware Requirements
- ESP32 DevKit V1 (or compatible ESP32 board)
- USB cable for programming
- (Optional) LED on GPIO 26

---

## Software Requirements
- [PlatformIO IDE](https://platformio.org/install)
- Arduino framework
- ESP32 board support via PlatformIO
- MQTT broker (e.g., Mosquitto on Kali Linux)

---

## Installation & Build
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd ESP32-Sniffer
   ```
2. Open in PlatformIO IDE.
3. Edit `src/include/config.h` to set your Wi-Fi and MQTT credentials.
4. Build and upload:
   ```bash
   pio run --target upload
   ```
5. Open Serial Monitor:
   ```bash
   pio device monitor
   ```

---

## Usage
- On boot, ESP32 starts as AP (`ESP32_Sniffer`, password: `12345678`) and (optionally) connects to your Wi-Fi as STA for MQTT.
- Connect to the AP and open `http://192.168.4.1/` for the web interface.
- Captured Wi-Fi frames are streamed to the configured MQTT broker.
- Web UI allows live monitoring and control of sniffer state.

---

## Code Structure
```
ESP32-Sniffer/
├─ src/
│   ├─ main.cpp             # Entry point, Wi-Fi/MQTT state, event handlers
│   ├─ wifi_sniffer.cpp     # Promiscuous mode, frame capture logic
│   ├─ streamer.cpp         # MQTT streaming, JSON conversion
│   ├─ web_interface.cpp    # Web server and UI handlers
│   ├─ globals.cpp          # Shared state, buffer, MQTT client
│   ├─ circular_buffer.cpp  # Circular buffer implementation
│   └─ include/
│       ├─ config.h             # Wi-Fi/MQTT/AP/STA configuration
│       ├─ wifi_sniffer.h       # Sniffer control prototypes
│       ├─ streamer.h           # Streamer/MQTT prototypes
│       ├─ web_interface.h      # Web server prototypes
│       ├─ globals.h            # Shared state, buffer, MQTT client
│       ├─ wifi_frame.h         # Wi-Fi frame struct
│       └─ circular_buffer.h    # Buffer class
├─ platformio.ini           # PlatformIO project config
├─ MQTT_SETUP_GUIDE.md      # Guide for MQTT setup (Kali Linux)
└─ Readme.md                # Project documentation
```

### Main Modules
- **main.cpp**: Wi-Fi/MQTT state, event handlers, main loop
- **wifi_sniffer.cpp**: Promiscuous mode, frame parsing, buffer
- **streamer.cpp**: Converts frames to JSON, streams to MQTT
- **web_interface.cpp**: HTTP server, web UI, scan controls
- **globals.cpp**: Shared state, buffer, MQTT client
- **circular_buffer.cpp**: Efficient frame storage
- **config.h**: All configuration (Wi-Fi, MQTT, AP/STA)

---

## Configuration
Edit `src/include/config.h` to set:
- Wi-Fi AP/STA credentials
- MQTT broker IP, port, topic
- Buffer size, LED pin, etc.

---

## MQTT Setup
See `MQTT_SETUP_GUIDE.md` for step-by-step instructions to set up an MQTT broker (e.g., Mosquitto on Kali Linux) and configure the ESP32.

---

## Safety Notice
**Use only on networks you own or have explicit permission to monitor. Unauthorized sniffing is illegal.**

---

## License
See LICENSE for details.


