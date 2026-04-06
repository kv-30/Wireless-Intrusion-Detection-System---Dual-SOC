# MQTT Setup Guide for Kali Linux

## Architecture
```
┌─────────────────┐         ┌────────────────┐
│   Kali Linux    │         │      ESP32     │
│ (MQTT Broker)   │◄────────►│   (WiFi SNR)   │
│  192.168.X.X    │   WiFi   │                │
└─────────────────┘         └────────────────┘
     ▲                            │
     │                            │ Also hosts AP
     │                            │
     └────────────────────────────┼───────────────────┐
                                  │   (192.168.4.1)   │
                         ┌────────▼─────────┐         │
                         │ Other WiFi Devs  │─────────┘
                         │ (Web Interface)  │
                         └──────────────────┘
```

## Setup Steps

### Step 1: Find Your WiFi Network
On Kali Linux, find your WiFi network name and password:
```bash
# List available WiFi networks
nmcli dev wifi list

# Or check current connection
nmcli connection show
```

### Step 2: Update ESP32 Configuration
Edit [src/config.h](src/config.h) and update these lines:

```cpp
#define ENABLE_STA_MODE 1                    // Already enabled (= 1)
#define WIFI_STA_SSID "your_wifi_ssid"       // ← CHANGE THIS (your WiFi name)
#define WIFI_STA_PASSWORD "your_wifi_pass"   // ← CHANGE THIS (your WiFi password)
#define MQTT_BROKER "192.168.0.108"          // ← CHANGE IF NEEDED (MQTT broker IP)
```

**Example:**
```cpp
#define WIFI_STA_SSID "MyKaliNetwork"
#define WIFI_STA_PASSWORD "MyPassword123"
#define MQTT_BROKER "192.168.1.100"  // Kali's IP on your network
```

### Step 3: Verify MQTT Broker is Running
```bash
# Check if MQTT is running (e.g., Mosquitto)
ps aux | grep mosquitto

# If not running, install and start it
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl start mosquitto
sudo systemctl enable mosquitto  # Auto-start on boot

# Verify it's listening
netstat -an | grep 1883
# Or: ss -tuln | grep 1883
```

### Step 4: Find Your Kali IP on the WiFi Network
```bash
# Get your Kali IP on the network where ESP32 will connect
ip addr show
# Look for inet address on your active WiFi interface (usually wlan0, wlp3s0, etc.)

# Example output:
# inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic noprefixroute wlan0
```

Update `MQTT_BROKER` in config.h to match your Kali IP.

### Step 5: Flash ESP32
```bash
# Build and upload to ESP32
pio run -t upload

# Monitor serial output
pio device monitor --baud 115200
```

### Step 6: Monitor Connection Progress
Watch the serial monitor output for:
```
[SETUP] ESP32 WiFi Sniffer starting...
[WiFi] Dual mode enabled (AP + STA)
[WiFi] AP started at IP: 192.168.4.1
[WiFi] Connecting to STA: MyKaliNetwork...
[MQTT] Broker set to 192.168.1.100:1883
...
[WiFi] Connected to WiFi network
[WiFi] Got IP address: 192.168.1.XXX
[MQTT] Attempting connection to 192.168.1.100:1883...
[MQTT] Connected successfully!
```

### Step 7: Test MQTT Connection
```bash
# In a terminal, subscribe to sniffer messages
mosquitto_sub -h 192.168.1.100 -t "wifi/sniffer"

# Start sniffing from web interface at 192.168.4.1
# You should see WiFi frame JSON messages arriving
```

## Two-Network Access

After flashing, ESP32 is accessible from **TWO networks**:

1. **Direct WiFi Connection (MQTT-enabled)**
   - Connect to your Kali WiFi network
   - Access MQTT via local IP (192.168.1.100)
   - Web interface: `http://192.168.1.XXX` (ESP32's IP on Kali network)

2. **AP Mode Connection (no MQTT)**
   - Connect to ESP32's AP: `ESP32_Sniffer` / `12345678`
   - Web interface: `http://192.168.4.1`
   - **Note:** No MQTT access from AP mode (isolated network)

## Troubleshooting

### MQTT Still Not Connecting?

**Check MQTT status:**
```bash
# Verify MQTT broker is running
sudo systemctl status mosquitto

# Check if mosquitto is listening on all interfaces
sudo mosquitto_pub -h 192.168.1.100 -t "test" -m "hello"
```

**Check ESP32 WiFi connection:**
- Look for `[WiFi] Got IP address:` in serial output
- If missing, verify SSID/password are correct

**Check firewall:**
```bash
# Temporarily disable firewall for testing
sudo ufw disable  # UFW firewall
# Or add rule for MQTT
sudo ufw allow 1883/tcp
```

**Verify IP addresses:**
```bash
# Ping ESP32 from Kali
ping 192.168.1.XXX  # ESP32's actual IP on your network

# Ping MQTT broker from another device
ping 192.168.1.100  # Kali's IP
```

### MQTT Error Codes (from serial monitor)
- `-4` = Server unavailable
- `-3` = Client ID rejected
- `-2` = No connection refused
- `-1` = Connection timeout

### WiFi Connection Timeout
The ESP32 waits 15 seconds for WiFi connection. If still connecting after setup:
- Check WIFI_STA_SSID and WIFI_STA_PASSWORD are correct
- Verify WiFi signal is strong
- Restart ESP32

## Reverting to AP-Only Mode
If you need AP-only mode without MQTT:
```cpp
#define ENABLE_STA_MODE 0  // Disable STA mode
```

## Security Notes
- MQTT on `192.168.0.108` defaults are unencrypted
- ESP32 AP password is `12345678` (consider changing in config)
- Use strong WiFi credentials in WIFI_STA_PASSWORD

---

**Happy sniffing!** 📡
