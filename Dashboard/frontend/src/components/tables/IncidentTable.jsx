// src/components/tables/IncidentTable.jsx
import React from "react";

export function IncidentTable({ frames = [], goldMetrics = [] }) {
  return (
    <table className="w-full text-sm border-collapse border border-gray-300 cyber-table">
      <thead>
        <tr className="cyber-table-head">
          <th>Time</th>
          <th>Src</th>
          <th>Dst</th>
          <th>State</th>
          <th>Attack</th>
          <th>Traffic (T)</th>
          <th>Avg RSSI (F)</th>
          <th>Entropy (A)</th>
        </tr>
      </thead>
      <tbody>
        {frames.map((f, idx) => {
          const gold = goldMetrics[idx] || {};
          const stateClass = gold.state === "ATTACK" ? "text-red-600 font-bold" : "";
          const attackType = gold.attack_type || (gold.attack_detected ? "DEAUTH_FLOOD" : "NONE");
          const attackClass = attackType !== "NONE" ? "text-red-600 font-bold" : "";
          const avgRssi = Number(gold.avg_rssi ?? 0);
          const entropy = Number(gold.entropy ?? 0);
          return (
            <tr key={idx} className="border-t border-gray-200 cyber-table-row">
              <td>{new Date(f._time || Date.now()).toLocaleTimeString()}</td>
              <td>{f.src || "N/A"}</td>
              <td>{f.dst || "N/A"}</td>
              <td className={stateClass}>{gold.state || "NORMAL"}</td>
              <td className={attackClass}>{attackType}</td>
              <td>{gold.traffic || 0}</td>
              <td>{avgRssi.toFixed(2)}</td>
              <td>{entropy.toFixed(2)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}