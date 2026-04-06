// wsService.js
export class WSService {
    constructor(url) {
        this.url = url;
        this.silverCallbacks = [];
        this.goldCallbacks = [];
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
            const layer = data.layer || "gold"; // default
            if(layer === "silver") {
                this.silverCallbacks.forEach(cb => cb(data));
            } else {
                this.goldCallbacks.forEach(cb => cb(data));
            }
        };
    }

    onSilver(cb) {
        this.silverCallbacks.push(cb);
    }

    onGold(cb) {
        this.goldCallbacks.push(cb);
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