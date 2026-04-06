# ESP32 Wi-Fi Demo

A sanitized ESP32 Wi-Fi web interface demo for public release. Core operation logic has been removed for IP protection while preserving build structure and UI flow.

---

## Features
- AP-mode web interface for scanning available Wi-Fi networks
- Placeholder controls for start/stop operations
- Configurable build constants through `platformio.ini`
- Modular source structure with separate headers and implementation files
- LED feedback hook included for visible status indication

---

## Hardware Requirements
- ESP32 DevKit V1 (or compatible ESP32 board)
- USB cable for programming
- (Optional) LED on GPIO 25

---

## Software Requirements
- [PlatformIO IDE](https://platformio.org/install)
- Arduino framework
- ESP32 board support via PlatformIO

---

## Installation & Build
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd ESP32-Deauther
   ```
2. Open the project in PlatformIO IDE.
3. Select your board in `platformio.ini` (default: `esp32doit-devkit-v1`).
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
- On boot, ESP32 starts in AP mode.
- Connect to the AP and open `http://192.168.4.1/` in your browser.
- Use the web interface to scan networks and control placeholder actions.
- This public release does not include actual network operation functionality.

---

## Code Structure
```
ESP32-Deauther/
├─ include/
│   ├─ deauth.h           # Public operation API definitions
│   ├─ definitions.h      # Configurable constants and macros
│   ├─ types.h            # Sanitized public types
│   └─ web_interface.h    # Web server API declarations
├─ src/
│   ├─ main.cpp           # Entry point, setup/loop
│   ├─ general.cpp        # LED and utility support
│   ├─ deauth.cpp         # Placeholder operation implementation
│   └─ web_interface.cpp  # Web interface implementation
├─ platformio.ini         # PlatformIO project configuration
└─ README.md              # Project documentation
```

### Main Modules
- **main.cpp**: Initializes hardware, starts the web server, and manages the main loop.
- **general.cpp**: LED and utility support routines.
- **deauth.cpp**: Sanitized operation placeholder implementation.
- **web_interface.cpp**: Web interface HTML, routes, and network scanning handlers.
- **definitions.h**: Runtime and build-time constants.
- **types.h**: Minimal public type definitions.
- **web_interface.h**: Exported web interface functions.

---

## Configuration
Edit `include/definitions.h` to change:
- AP SSID/password
- LED and build configuration settings

---

## Safety Notice
This repository is intended for safe public release. Core operation logic has been removed, and the current code should be treated as a structural demo.

---

## License
See LICENSE for details.


