// wsService.js
// Core logic removed for IP protection.
// WebSocket message routing logic has been abstracted for public release.

export class WSService {
    constructor(url) {
        this.url = url;
        this.callbacks = [];
        this.reconnectTimer = null;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onclose = () => {
            this.reconnectTimer = setTimeout(() => this.connect(), 2000);
        };
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // Generic message callback - layer routing has been removed
            this.callbacks.forEach(cb => cb(data));
        };
    }

    onMessage(cb) {
        this.callbacks.push(cb);
    }

    close() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
        }
        if (this.ws) {
            this.ws.close();
        }
    }
}