
---

```markdown
# frontend/README.md

# Frontend - Wireless IDS Dashboard

This folder contains the frontend dashboard of the Wireless IDS project.  
It provides a **real-time monitoring UI** for:

1. Wi-Fi traffic metrics (frame counts, RSSI, entropy)
2. Attack predictions (from ML microservice)
3. Alerts for suspicious activity
4. Historical playback of network data

## Folder Structure

frontend/
├── public/                    # Static assets (index.html, favicon)
├── src/
│   ├── app/
│   │   └── store.js           # Global state (Redux/Zustand/Context)
│   ├── pages/
│   │   └── Dashboard.jsx      # Main dashboard page
│   ├── components/
│   │   ├── charts/            # Line charts, heatmaps
│   │   ├── tables/            # Raw frames table
│   │   ├── alerts/            # Alert banners
│   │   ├── controls/          # Filters and sliders
│   │   └── layout/            # Dashboard layout wrapper
│   ├── services/
│   │   ├── wsService.js       # WebSocket client
│   │   └── apiService.js      # REST API client for historical data
│   ├── hooks/
│   │   ├── useWebSocket.js
│   │   ├── useStreamBuffer.js
│   │   ├── useHistoricalData.js
│   │   └── useFilters.js
│   ├── utils/
│   │   ├── time.js
│   │   └── format.js
│   ├── styles/
│   │   └── theme.css
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── README.md

## Running Locally

```bash
cd frontend
npm install
npm run dev