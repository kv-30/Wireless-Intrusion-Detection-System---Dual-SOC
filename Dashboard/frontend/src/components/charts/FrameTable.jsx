
import React from "react";

export function FrameTable({ frames = [], goldMetrics = [] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Traffic</th>
          <th>Avg RSSI</th>
          <th>Entropy</th>
          <th>State</th>
          <th>Attack Type</th>
          <th>Src</th>
          <th>Dst</th>
        </tr>
      </thead>
      <tbody>
        {frames.map((f, idx) => {
          const gold = goldMetrics[idx] || {};
          return (
            <tr key={idx}>
              <td>{new Date(f._time || Date.now()).toLocaleTimeString()}</td>
              <td>{gold.traffic || 0}</td>
              <td>{gold.avg_rssi?.toFixed(2) || 0}</td>
              <td>{gold.entropy?.toFixed(2) || 0}</td>
              <td>{gold.state || "NORMAL"}</td>
              <td>{gold.attack_type || "NONE"}</td>
              <td>{f.src || "N/A"}</td>
              <td>{f.dst || "N/A"}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}