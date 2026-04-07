import React from "react";
import DashboardLayout from "../components/layout/DashboardLayout";
import { useWebSocket } from "../hooks/useWebSocket";
import { TrafficChart } from "../components/charts/TrafficChart";
import { RSSIChart } from "../components/charts/RSSIChart";
import { EntropyChart } from "../components/charts/EntropyChart";
import { AlertStateChart } from "../components/charts/AlertStateChart";
import { NumericCard } from "../components/cards/NumericCard";
import { IncidentTable } from "../components/tables/IncidentTable";
import AlertBanner from "../components/alerts/AlertBanner";
import { useStore } from "../app/store";
import { resolveWsUrl } from "../utils/endpoints";

export default function Dashboard() {
  // Core logic removed for IP protection.
  // Data layer abstractions applied to metrics display.
  const { silverData = [], goldData = [] } = useWebSocket(resolveWsUrl());
  const { connectionStatus } = useStore();

  const latest = goldData.length > 0 ? goldData[goldData.length - 1] : {};
  const metric1 = Number(latest.metric_value_1 || 0);
  const metric2 = Number(latest.metric_value_2 || 0);
  const metric3 = Number(latest.metric_value_3 || 0);
  const state = latest.state || "NORMAL";
  const detectionType = latest.detection_type || (latest.detection ? "DETECTED" : "NORMAL");
  const baseline = Number(latest.baseline || 0);
  const isAlert = state === "ALERT";

  return (
    <DashboardLayout>
      <div className="min-h-screen text-white p-2">
      <div className="mb-6">
        <h1 className="text-3xl font-bold cyber-title">System Monitoring Dashboard</h1>
        <p className="text-xs mt-1 text-gray-300 cyber-status-center">
          Stream: {connectionStatus === "connected" ? "🟢 Connected" : connectionStatus === "error" ? "🔴 Error" : "🟠 Reconnecting"}
        </p>
        <p className="text-xs mt-1 text-gray-300 cyber-status-center">
          Preview: Data points={goldData.length} | Stream events={silverData.length}
        </p>
      </div>

      <AlertBanner state={state} confidence={latest.confidence || 0} />

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <NumericCard label="Metric 1" value={metric1} highlight={metric1 > baseline * 1.5} />
        <NumericCard label="Metric 2" value={metric2.toFixed(2)} />
        <NumericCard label="Metric 3" value={metric3.toFixed(2)} />
        <NumericCard label="State" value={state} color={isAlert ? "red" : "green"} />
        <NumericCard label="Detection" value={detectionType} highlight={isAlert} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-[#1a2338] p-4 rounded-xl">
          <TrafficChart data={goldData} baseline={baseline} />
        </div>
        <div className="bg-[#1a2338] p-4 rounded-xl">
          <RSSIChart data={goldData} />
        </div>
        <div className="bg-[#1a2338] p-4 rounded-xl">
          <EntropyChart data={goldData} />
        </div>
        <div className="bg-[#1a2338] p-4 rounded-xl">
          <AlertStateChart data={goldData} />
        </div>
      </div>

      <div className="bg-[#1a2338] p-4 rounded-xl">
        <h2 className="text-lg text-white mb-3">📊 Event Log</h2>
        {silverData.length === 0 ? (
          <div className="text-gray-300 text-sm">
            Waiting for events... Live telemetry will appear here.
          </div>
        ) : (
          <IncidentTable frames={silverData.slice(-20)} goldMetrics={goldData.slice(-20)} />
        )}
      </div>
      </div>
    </DashboardLayout>
  );
}