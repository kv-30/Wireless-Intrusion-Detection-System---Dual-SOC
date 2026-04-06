import React from "react";

export default function AlertBanner({ state = "NORMAL", confidence = 0 }) {
  if (state !== "ATTACK") {
    return (
      <div className="cyber-alert cyber-alert-normal px-4 py-3 rounded mb-4">
        ✅ System state: NORMAL
      </div>
    );
  }

  return (
    <div className="cyber-alert cyber-alert-attack px-4 py-3 rounded mb-4">
      🚨 Attack detected ({(Number(confidence || 0) * 100).toFixed(1)}% confidence)
    </div>
  );
}