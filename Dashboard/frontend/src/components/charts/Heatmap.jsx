import React from "react";

export default function Heatmap({ data }) {
  // Placeholder: implement d3 or react-heatmap-grid
  return (
    <div>
      <h4>Client-AP Heatmap (placeholder)</h4>
      <pre>{JSON.stringify(data.slice(-5), null, 2)}</pre>
    </div>
  );
}