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

function normalizeGoldPoint(point = {}) {
  const rawState = String(point.state || "").toUpperCase();
  const label = String(
    point.ml_prediction_label || point.prediction_label || ""
  ).toLowerCase();
  const predictionCode = toNumber(
    point.ml_prediction_code ?? point.prediction_code,
    0
  );
  const attackDetected =
    toBool(point.attack_detected) || label === "attack" || predictionCode === 1;

  const state =
    rawState === "ATTACK" || rawState === "NORMAL"
      ? rawState
      : attackDetected
        ? "ATTACK"
        : "NORMAL";

  const confidence = toNumber(
    point.ml_confidence ?? point.prob_attack ?? point?.probabilities?.prob_attack,
    0
  );

  return {
    ...point,
    state,
    attack_detected: attackDetected,
    ml_confidence: confidence,
    attack_type: point.attack_type || (attackDetected ? "DEAUTH_FLOOD" : "NONE"),
  };
}

export function useWebSocket(wsUrl) {
  const [silverData, setSilverData] = useState([]);
  const [goldData, setGoldData] = useState([]);
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
  const BRONZE_WINDOW_SECONDS = 30;
  const GOLD_WINDOW_SECONDS = 30;
  const POLL_INTERVAL_MS = 2000;

  const withRangeParams = (url, seconds) => {
    const params = new URLSearchParams(buildRangeParams(seconds));
    return `${url}?${params.toString()}`;
  };

  useEffect(() => {
    let mounted = true;

    const loadInitial = async () => {
      try {
        const [silverRes, goldRes] = await Promise.all([
          fetch(withRangeParams(`${apiBase}/bronze`, BRONZE_WINDOW_SECONDS)),
          fetch(withRangeParams(`${apiBase}/gold`, GOLD_WINDOW_SECONDS)),
        ]);

        const silverJson = silverRes.ok ? await silverRes.json() : [];
        const goldJson = goldRes.ok ? await goldRes.json() : [];

        if (!mounted) return;
        const silver = Array.isArray(silverJson) ? silverJson.reverse() : [];
        const gold = Array.isArray(goldJson)
          ? goldJson.reverse().map(normalizeGoldPoint)
          : [];
        setSilverData(silver);
        setGoldData(gold);
        setLiveData({ silver, gold });
      } catch (err) {
        console.error("Initial data fetch failed:", err);
      }
    };

    loadInitial();

    const refreshSilver = setInterval(async () => {
      try {
        const res = await fetch(withRangeParams(`${httpBase}/api/bronze`, BRONZE_WINDOW_SECONDS));
        if (!res.ok) return;
        const data = await res.json();
        if (mounted && Array.isArray(data)) {
          const silver = data.reverse().slice(-300);
          setSilverData(silver);
          setLiveData({ silver });
        }
      } catch (_) {
        // Keep stream alive even if polling fails
      }
    }, POLL_INTERVAL_MS);

    // Fallback polling for gold metrics in case websocket is blocked/interrupted
    const refreshGold = setInterval(async () => {
      try {
        const res = await fetch(withRangeParams(`${httpBase}/api/gold`, GOLD_WINDOW_SECONDS));
        if (!res.ok) return;
        const data = await res.json();
        if (mounted && Array.isArray(data)) {
          const gold = data.reverse().slice(-300).map(normalizeGoldPoint);
          setGoldData(gold);
          setLiveData({ gold });
        }
      } catch (_) {
        // Keep stream alive even if polling fails
      }
    }, POLL_INTERVAL_MS);

    return () => {
      mounted = false;
      clearInterval(refreshSilver);
      clearInterval(refreshGold);
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
          if (parsed?.layer && parsed.layer !== "gold") {
            return;
          }
          const normalized = normalizeGoldPoint(parsed);
          setGoldData((prev) => {
            const next = [...prev, normalized].slice(-300);
            setLiveData({ gold: next });
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

  return { silverData, goldData };
}