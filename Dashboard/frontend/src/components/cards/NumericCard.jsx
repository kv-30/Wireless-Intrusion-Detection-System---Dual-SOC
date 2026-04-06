
import React from "react";

export function NumericCard({ label, value, highlight = false, color = "default" }) {
  const borderClass =
    highlight || color === "red"
      ? "border-red-500"
      : color === "green"
      ? "border-green-500"
      : "border-blue-500";

  const valueClass =
    highlight || color === "red"
      ? "text-red-300"
      : color === "green"
      ? "text-green-300"
      : "text-white";

  return (
    <div className={`glass-panel p-4 rounded-xl border-l-4 ${borderClass}`}>
      <span className="text-xs font-mono text-gray-300 uppercase">{label}</span>
      <div className={`text-3xl font-bold mt-1 ${valueClass}`}>{value}</div>
    </div>
  );
}