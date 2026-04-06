import React from "react";

export default function FrameTable({ frames }) {
  return (
    <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>SRC</th>
          <th>DST</th>
          <th>RSSI</th>
          <th>Subtype</th>
        </tr>
      </thead>
      <tbody>
        {frames.slice(-20).reverse().map((f, idx) => (
          <tr key={idx}>
            <td>{new Date(f.ts * 1000).toLocaleTimeString()}</td>
            <td>{f.src}</td>
            <td>{f.dst}</td>
            <td>{f.rssi}</td>
            <td>{f.subtype}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}