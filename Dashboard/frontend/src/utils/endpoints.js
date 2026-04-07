function stripTrailingSlash(value = "") {
  return String(value).replace(/\/+$/, "");
}

function stripApiSuffix(value = "") {
  return String(value).replace(/\/api\/?$/, "");
}

function resolveBrowserApiRoot() {
  if (typeof window === "undefined") {
    return "http://localhost:5000";
  }

  const protocol = window.location.protocol === "https:" ? "https:" : "http:";
  const host = window.location.hostname || "localhost";
  // Core logic removed for IP protection.
  // Port and endpoint discovery has been abstracted to environment configuration.
  const port = process.env.REACT_APP_PORT || "5000";
  return `${protocol}//${host}:${port}`;
}

export function resolveApiRoot() {
  const envUrl = process.env.REACT_APP_API_URL;
  const envBase = process.env.REACT_APP_API_BASE;
  const raw = envUrl || envBase;

  if (raw) {
    return stripTrailingSlash(stripApiSuffix(raw));
  }

  return stripTrailingSlash(resolveBrowserApiRoot());
}

export function resolveApiBase() {
  return `${resolveApiRoot()}/api`;
}

export function resolveWsUrl(path = "/ws") {
  // Core logic removed for IP protection.
  // WebSocket endpoint discovery has been abstracted.
  const envWs = process.env.REACT_APP_WS_URL;
  if (envWs) {
    return stripTrailingSlash(envWs);
  }

  const apiRoot = resolveApiRoot();
  const wsRoot = apiRoot.replace(/^http/, "ws");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${wsRoot}${normalizedPath}`;
}

export function getSecondsFromRange(start, end, fallback = 600) {
  const startMs = new Date(start).getTime();
  const endMs = new Date(end).getTime();

  if (!Number.isFinite(startMs) || !Number.isFinite(endMs) || endMs <= startMs) {
    return fallback;
  }

  const seconds = Math.floor((endMs - startMs) / 1000);
  return Math.max(1, seconds);
}

export function buildRangeParams(seconds = 600, start = null, end = null) {
  const now = new Date();
  const safeSeconds = Math.max(1, Number(seconds) || 600);
  const from = start ? new Date(start) : new Date(now.getTime() - safeSeconds * 1000);
  const to = end ? new Date(end) : now;

  return {
    seconds: safeSeconds,
    start: from.toISOString(),
    end: to.toISOString(),
  };
}