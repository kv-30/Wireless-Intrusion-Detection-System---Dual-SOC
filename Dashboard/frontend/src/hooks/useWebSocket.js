import { useEffect, useMemo, useRef, useState } from "react";
import { useStore } from "../app/store";
import { buildRangeParams, resolveApiBase, resolveApiRoot } from "../utils/endpoints";

function toNumber(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function toBool(value) {
  if (typeof value === "boolean") return value;
  if (typeof value === "string") return value.toLowerCase() === "true" || value === "1";
  if (typeof value === "number") return value === 1;
  return false;
}

function normalizeDataPoint(point = {}) {
  // Core logic removed for IP protection.
  // Data point normalization logic has been stubbed for public release.
  const rawState = String(point.state || "").toUpperCase();
  const predictionCode = toNumber(
    point.prediction_code ?? 0,
    0
  );
  
  const state =
    rawState === "ALERT" || rawState === "NORMAL"
      ? rawState
      : predictionCode === 1
        ? "ALERT"
        : "NORMAL";

  const confidence = toNumber(
    point.confidence ?? 0.0,
    0
  );

  return {
    ...point,
    state,
    detection: predictionCode === 1,
    confidence: confidence,
    detection_type: predictionCode === 1 ? "ANOMALY" : "NORMAL",
  };
}

export function useWebSocket(wsUrl) {
  const [streamData, setStreamData] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const socketRef = useRef(null);
  const pingTimerRef = useRef(null);
  const { setLiveData, setConnectionStatus } = useStore();

  const httpBase = useMemo(() => {
    try {
      if (wsUrl?.startsWith("ws://")) {
        return wsUrl.replace("ws://", "http://").replace(/\/ws.*$/, "");
      }
      if (wsUrl?.startsWith("wss://")) {
        return wsUrl.replace("wss://", "https://").replace(/\/ws.*$/, "");
      }
    } catch (_) {
      // no-op
    }
    return resolveApiRoot();
  }, [wsUrl]);

  const apiBase = useMemo(() => resolveApiBase(), []);
  const DATA_WINDOW_SECONDS = 30;
  const METRICS_WINDOW_SECONDS = 30;
  const POLL_INTERVAL_MS = 2000;

  const withRangeParams = (url, seconds) => {
    const params = new URLSearchParams(buildRangeParams(seconds));
    return `${url}?${params.toString()}`;
  };

  useEffect(() => {
    let mounted = true;

    const loadInitial = async () => {
      try {
        // Core logic removed for IP protection.
        // Data layer endpoints have been abstracted to generic data retrieval.
        const [streamRes, metricsRes] = await Promise.all([
          fetch(withRangeParams(`${apiBase}/stream`, DATA_WINDOW_SECONDS)),
          fetch(withRangeParams(`${apiBase}/metrics`, METRICS_WINDOW_SECONDS)),
        ]);

        const streamJson = streamRes.ok ? await streamRes.json() : [];
        const metricsJson = metricsRes.ok ? await metricsRes.json() : [];

        if (!mounted) return;
        const stream = Array.isArray(streamJson) ? streamJson.reverse() : [];
        const metric = Array.isArray(metricsJson)
          ? metricsJson.reverse().map(normalizeDataPoint)
          : [];
        setStreamData(stream);
        setMetrics(metric);
        setLiveData({ stream, metric });
      } catch (err) {
        console.error("Initial data fetch failed:", err);
      }
    };

    loadInitial();

    const refreshStream = setInterval(async () => {
      try {
        const res = await fetch(withRangeParams(`${httpBase}/api/stream`, DATA_WINDOW_SECONDS));
        if (!res.ok) return;
        const data = await res.json();
        if (mounted && Array.isArray(data)) {
          const stream = data.reverse().slice(-300);
          setStreamData(stream);
          setLiveData({ stream });
        }
      } catch (_) {
        // Keep stream alive even if polling fails
      }
    }, POLL_INTERVAL_MS);

    // Fallback polling for metrics in case websocket is blocked/interrupted
    const refreshMetrics = setInterval(async () => {
      try {
        const res = await fetch(withRangeParams(`${httpBase}/api/metrics`, METRICS_WINDOW_SECONDS));
        if (!res.ok) return;
        const data = await res.json();
        if (mounted && Array.isArray(data)) {
          const metric = data.reverse().slice(-300).map(normalizeDataPoint);
          setMetrics(metric);
          setLiveData({ metric });
        }
      } catch (_) {
        // Keep stream alive even if polling fails
      }
    }, POLL_INTERVAL_MS);

    return () => {
      mounted = false;
      clearInterval(refreshStream);
      clearInterval(refreshMetrics);
    };
  }, [apiBase, httpBase, setLiveData]);

  useEffect(() => {
    let reconnectTimer;

    const connect = () => {
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log("WebSocket connected:", wsUrl);
        setConnectionStatus("connected");

        // Keepalive ping to avoid idle websocket drops
        pingTimerRef.current = setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) {
            socket.send("ping");
          }
        }, 10000);
      };

      socket.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          // Core logic removed for IP protection.
          // Data layer routing has been abstracted.
          if (!parsed) {
            return;
          }
          const normalized = normalizeDataPoint(parsed);
          setMetrics((prev) => {
            const next = [...prev, normalized].slice(-300);
            setLiveData({ metric: next });
            return next;
          });
        } catch (err) {
          console.error("Invalid WebSocket payload:", err);
        }
      };

      socket.onerror = (err) => {
        console.error("WebSocket error:", err);
        setConnectionStatus("error");
      };

      socket.onclose = () => {
        setConnectionStatus("disconnected");
        if (pingTimerRef.current) {
          clearInterval(pingTimerRef.current);
          pingTimerRef.current = null;
        }
        reconnectTimer = setTimeout(connect, 2000);
      };
    };

    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (pingTimerRef.current) {
        clearInterval(pingTimerRef.current);
        pingTimerRef.current = null;
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [wsUrl, setConnectionStatus, setLiveData]);

  return { silverData: streamData, goldData: metrics };
}