#include <Arduino.h>
#include <WebServer.h>
#include <WiFi.h>
#include "web_interface.h"
#include "wifi_sniffer.h"
#include "wifi_frame.h"
#include "globals.h"

WebServer server(80);

// ----------------------------
// Globals
// ----------------------------
int num_networks = 0;
bool wifi_scan_in_progress = false;  // Track async WiFi scan state

// ----------------------------
// Helpers
// ----------------------------
String getEncryptionType(wifi_auth_mode_t encryptionType) {
    switch (encryptionType) {
        case WIFI_AUTH_OPEN: return "Open";
        case WIFI_AUTH_WEP: return "WEP";
        case WIFI_AUTH_WPA_PSK: return "WPA_PSK";
        case WIFI_AUTH_WPA2_PSK: return "WPA2_PSK";
        case WIFI_AUTH_WPA_WPA2_PSK: return "WPA_WPA2_PSK";
        default: return "UNKNOWN";
    }
}

    #ifdef REMOVE_CORE_LOGIC
    // Core logic removed for IP protection
    #endif


// ----------------------------
// ROOT PAGE
// ----------------------------
void handle_root() {
    String html = R"HTML(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ESP32 Wi-Fi Sniffer</title>
<style>
body { background:#0a0a0a; color:#00ffcc; font-family:monospace; padding:20px;}
table { width:100%; border-collapse:collapse;}
th,td { border:1px solid #00ffcc; padding:8px;}
button { background:#00ffcc; border:none; padding:8px; cursor:pointer;}
tr:nth-child(even){ background:#001111; }
tr:hover{ background:#002222; }
</style>
<script>
var scanning = false;
function rescan(){
    scanning = true;
    document.getElementById("nets").innerHTML='<tr><td colspan="6" style="text-align:center;">Starting scan...</td></tr>';
    fetch('/rescan').then(()=>{
        pollNetworks();  // Start polling for results
    });
}
function pollNetworks(){
    fetch('/networks')
    .then(r=>r.text())
    .then(html=>{
        document.getElementById("nets").innerHTML=html;
        // If still scanning, poll again in 1 second
        if(html.includes('Scanning')){
            setTimeout(pollNetworks, 1000);
        } else {
            scanning = false;
        }
    });
}
function startSniff(ch){ fetch('/start?ch='+ch); }
function stopSniff(){ fetch('/stop'); }

window.onload=function(){
    // Do NOT auto-scan networks on page load
    // User must click Rescan button to fetch networks
    document.getElementById("nets").innerHTML='<tr><td colspan="6" style="text-align:center; padding:20px;">Click "Rescan Networks" to scan</td></tr>';
};
</script>
</head>
<body>

<h2>WiFi Networks</h2>
<button onclick="rescan()">Rescan Networks</button>

<table>
<tr><th>#</th><th>SSID</th><th>BSSID</th><th>CH</th><th>RSSI</th><th>Action</th></tr>
<tbody id="nets"></tbody>
</table>

<br>
<button onclick="stopSniff()">Stop Sniffing</button>

<h2>Captured Frames (latest 50)</h2>
<div style="height:300px; overflow-y:auto; border:1px solid #00ffcc;">
<table id="frames" style="width:100%; border-collapse:collapse;">
<thead>
<tr><th>Timestamp</th><th>SRC</th><th>DST</th><th>BSSID</th><th>RSSI</th><th>Subtype</th></tr>
</thead>
<tbody id="frameBody">
</tbody>
</table>
</div>

<script>
async function fetchFrames(){
    const resp=await fetch('/frames');
    const data=await resp.json();
    const tbody=document.getElementById("frameBody");
    
    // Append new frames at bottom
    data.forEach(f=>{
        // Check if we already have 50+ rows
        if(tbody.children.length >= 50) {
            // Remove oldest row (first child)
            tbody.removeChild(tbody.firstChild);
        }
        
        // Append new row at bottom
        const row = document.createElement('tr');
        row.innerHTML = '<td>'+f.ts+'</td><td>'+f.src+'</td><td>'+f.dst+'</td><td>'+f.bssid+'</td><td>'+f.rssi+'</td><td>'+f.subtype+'</td>';
        tbody.appendChild(row);
    });
}
setInterval(fetchFrames,1000);
</script>

</body>
</html>
)HTML";

    server.send(200,"text/html",html);
}

// ----------------------------
// START / STOP HANDLERS
// ----------------------------
void handle_start() {
    if(!server.hasArg("ch")){
        server.send(400,"text/plain","Missing channel");
        return;
    }
    int ch=server.arg("ch").toInt();
    start_sniffer(ch);
    sniffing_active=true;
    server.send(200,"text/plain","Sniffing started on channel "+String(ch));
}

void handle_stop() {
    stop_sniffer();
    sniffing_active=false;
    server.send(200,"text/plain","Sniffing stopped");
}

// ----------------------------
// NETWORK SCAN (Non-blocking async mode)
// ----------------------------
void handle_rescan() {
    // Start async scan - this won't block the main loop
    if(!wifi_scan_in_progress) {
        wifi_scan_in_progress = true;
        WiFi.scanNetworks(true);  // async=true, non-blocking - just call it, don't store return value
        Serial.println("[Web] Started async WiFi scan");
    } else {
        Serial.println("[Web] Scan already in progress, ignoring rescan request");
    }
    server.send(200,"text/plain","Scan started");
}

void handle_networks() {
    String rows="";
    
    // Check if scan is complete
    int scanResult = WiFi.scanComplete();
    if(scanResult == WIFI_SCAN_RUNNING) {
        rows = "<tr><td colspan='6' style='text-align:center; padding:20px;'>Scanning... please wait</td></tr>";
        Serial.println("[Web] Scan still running, waiting...");
        server.send(200,"text/html",rows);
        return;
    }
    
    // Scan complete - get results
    if(scanResult >= 0) {
        wifi_scan_in_progress = false;
        num_networks = scanResult;
        Serial.printf("[Web] Scan complete! Found %d networks\n", scanResult);
    } else if(scanResult == -1) {
        Serial.println("[Web] ERROR: Scan never started (return -1)");
    } else {
        Serial.printf("[Web] ERROR: Unknown scan result: %d\n", scanResult);
    }
    
    // Display networks
    if(num_networks == 0) {
        rows = "<tr><td colspan='6' style='text-align:center; padding:20px;'>No networks found</td></tr>";
    } else {
        for(int i=0;i<num_networks;i++){
            rows+="<tr>";
            rows+="<td>"+String(i)+"</td>";
            rows+="<td>"+WiFi.SSID(i)+"</td>";
            rows+="<td>"+WiFi.BSSIDstr(i)+"</td>";
            rows+="<td>"+String(WiFi.channel(i))+"</td>";
            rows+="<td>"+String(WiFi.RSSI(i))+"</td>";
            rows+="<td><button onclick='startSniff("+String(WiFi.channel(i))+")'>Sniff</button></td>";
            rows+="</tr>";
        }
    }
    server.send(200,"text/html",rows);
}

// ----------------------------
// FRAMES
// ----------------------------
void handle_frames(){
    String json="[";
    WiFiFrame frame;
    bool first=true;
    size_t n = frameBuffer.size()>50 ? 50 : frameBuffer.size();
    for(size_t i=0;i<n;i++){
        if(!frameBuffer.pop(frame)) break;
        if(!first) json+=",";
        first=false;
        json+="{\"ts\":"+String(frame.timestamp)+
              ",\"src\":\""+macToStr(frame.src)+"\""+
              ",\"dst\":\""+macToStr(frame.dst)+"\""+
              ",\"bssid\":\""+macToStr(frame.bssid)+"\""+
              ",\"rssi\":"+String(frame.rssi)+
              ",\"subtype\":"+String(frame.subtype)+"}";
    }
    json+="]";
    server.send(200,"application/json",json);
}

// ----------------------------
// INIT
// ----------------------------
void init_web_interface(){
    // WiFi AP already configured in main.cpp setup()
    // Just register endpoints
    server.on("/",handle_root);
    server.on("/start",handle_start);
    server.on("/stop",handle_stop);
    server.on("/rescan",handle_rescan);
    server.on("/networks",handle_networks);
    server.on("/frames",handle_frames);

    server.begin();
    Serial.println("Web UI ready at http://192.168.4.1");
}

void web_interface_handle_client(){
    server.handleClient();
}