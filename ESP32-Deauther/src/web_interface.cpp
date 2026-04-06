#include <Arduino.h>
#include <WebServer.h>
#include <WiFi.h>
#include "web_interface.h"
#include "definitions.h"
#include "deauth.h"

WebServer server(80);

// Global state
static int num_networks = 0;
static String current_network_name;
static bool wifi_scan_in_progress = false;  // Track async WiFi scan state

// ----------------------------
// ROOT PAGE
// ----------------------------
void handle_root() {
    String html = R"HTML(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ESP32 Wi-Fi Demo</title>

<style>
body {
    background: #0a0a0a;
    color: #ff0000;
    font-family: 'Courier New', Courier, monospace;
    padding: 20px;
    margin: 0;
}

h2 {
    text-align: center;
    font-size: 2.5em;
    color: #ff0000;
    text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #ff0000;
    padding: 12px;
    text-align: center;
    font-size: 1.1em;
}

th {
    background-color: #1a1a1a;
    color: #ff0000;
    text-shadow: 0 0 5px #ff0000;
}

tr:nth-child(even) {
    background-color: #111;
}

tr:hover {
    background-color: #333;
}

button {
    background: #ff0000;
    border: none;
    padding: 12px;
    color: black;
    font-size: 1.1em;
    cursor: pointer;
    border-radius: 5px;
    transition: all 0.3s ease;
    box-shadow: 0 0 5px #ff0000, 0 0 15px #ff0000;
}

button:disabled {
    background: #555;
    cursor: not-allowed;
}

button:hover {
    background: #cc0000;
    box-shadow: 0 0 10px #cc0000, 0 0 20px #cc0000;
}

button.running {
    background: red !important;
    color: white;
    box-shadow: 0 0 10px red, 0 0 30px red;
}

.message {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #ff0000;
    color: black;
    padding: 10px;
    font-size: 1.2em;
    text-align: center;
    display: none;
    z-index: 9999;
    animation: fadeOut 3s forwards;
    text-shadow: 0 0 10px #ff0000;
}

@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; transform: translateY(-50px); }
}
</style>

<script>
function rescan(){
    document.getElementById("nets").innerHTML =
    '<tr><td colspan="6" style="text-align:center;">Scanning...</td></tr>';
    document.getElementById("message").style.display = "none";  // Hide any old message

    fetch('/rescan').then(()=>{
        setTimeout(loadNetworks, 500);
    });
}

function loadNetworks(){
    fetch('/networks')
    .then(r=>r.text())
    .then(html=>{
        document.getElementById("nets").innerHTML = html;
    });
}

function startAction(num){
    fetch('/execute?net_num='+num)
    .then(r=>r.text())
    .then(msg=>{
        showMessage(msg);
        loadNetworks();
    });
}

function stopAction(){
    fetch('/stop')
    .then(r=>r.text())
    .then(msg=>{
        showMessage(msg);
        loadNetworks();
    });
}

function showMessage(msg) {
    const messageElement = document.getElementById("message");
    messageElement.textContent = msg;
    messageElement.style.display = "block";
    setTimeout(function(){
        messageElement.style.display = "none";
    }, 9000);
}

window.onload=function(){
    document.getElementById("nets").innerHTML =
    '<tr><td colspan="6" style="text-align:center;">Click Rescan</td></tr>';
};
</script>
</head>

<body>

<h2>WiFi Networks</h2>
<button onclick="rescan()">Rescan Networks</button>

<div id="message" class="message"></div> <!-- For message display -->

<table>
<tr>
<th>#</th><th>SSID</th><th>BSSID</th><th>CH</th><th>RSSI</th><th>Action</th>
</tr>
<tbody id="nets"></tbody>
</table>

<br>
<button onclick="stopAction()">Stop Action</button>

</body>
</html>
)HTML";

    server.send(200, "text/html", html);
}

// ----------------------------
// NETWORK TABLE (DYNAMIC)
// ----------------------------
void handle_networks() {
    String rows = "";

    for (int i = 0; i < num_networks; i++) {
        String ssid = WiFi.SSID(i);

        bool isCurrent = operation_in_progress && (ssid == current_network_name);

        String button;

        if (operation_in_progress) {
            if (isCurrent) {
                button = "<button class='running' disabled>Running</button>";
            } else {
                button = "<button disabled>Disabled</button>";
            }
        } else {
            button = "<button onclick='startAction(" + String(i) + ")'>Start</button>";
        }

        rows += "<tr><td>" + String(i) + "</td><td>" + ssid + "</td><td>" +
                WiFi.BSSIDstr(i) + "</td><td>" + String(WiFi.channel(i)) +
                "</td><td>" + String(WiFi.RSSI(i)) + "</td><td>" +
                button + "</td></tr>";
    }

    server.send(200, "text/html", rows);
}

// ----------------------------
// RESCAN
// ----------------------------
void handle_rescan() {
    num_networks = WiFi.scanNetworks();
    server.send(200, "text/plain", "OK");
}

// ----------------------------
// START ACTION
// ----------------------------
void handle_execute() {
    if (operation_in_progress) {
        server.send(200, "text/plain", "Action already running on " + current_network_name);
        return;
    }

    if (!server.hasArg("net_num")) {
        server.send(200, "text/plain", "Missing net_num");
        return;
    }

    int wifi_number = server.arg("net_num").toInt();

    if (wifi_number < 0 || wifi_number >= num_networks) {
        server.send(200, "text/plain", "Invalid network");
        return;
    }

    current_network_name = WiFi.SSID(wifi_number);

    start_operation(wifi_number, ACTION_TYPE_SINGLE, ACTION_DURATION, ACTION_RATE, NUM_BOTS, nullptr, 0);

    server.send(200, "text/plain", "Started action on " + current_network_name);
}

// ----------------------------
// STOP ACTION
// ----------------------------
void handle_stop() {
    if (!operation_in_progress) {
        server.send(200, "text/plain", "No action running");
        return;
    }

    stop_operation();

    server.send(200, "text/plain", "Stopped action on " + current_network_name);
}

// ----------------------------
// SERVER INIT
// ----------------------------
void start_web_interface() {
    server.on("/", handle_root);
    server.on("/networks", HTTP_GET, handle_networks);
    server.on("/rescan", HTTP_GET, handle_rescan);
    server.on("/execute", HTTP_GET, handle_execute);
    server.on("/stop", HTTP_GET, handle_stop);

    server.begin();
}

void web_interface_handle_client() {
    server.handleClient();
}