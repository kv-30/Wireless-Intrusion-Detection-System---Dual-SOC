// src/hooks/useStreamBuffer.js
import { useState, useEffect } from "react";
import { WSService } from "../services/wsService";
import { resolveWsUrl } from "../utils/endpoints";

export const useStreamBuffer = () => {
  const [buffer, setBuffer] = useState([]);

  useEffect(() => {
    // Create the WebSocket service
    const ws = new WSService(resolveWsUrl());

    // Listen for messages from both layers
    ws.onGold((data) => setBuffer((prev) => [...prev, data].slice(-500)));
    ws.onSilver((data) => setBuffer((prev) => [...prev, data].slice(-500)));

    // Cleanup on unmount
    return () => {
      ws.close();
    };
  }, []);

  return [buffer];
};