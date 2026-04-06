import React, { useState } from "react";

export default function FilterPanel({ onFilter }) {
  const [mac, setMac] = useState("");

  const handleApply = () => {
    onFilter({ mac });
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Filter by MAC"
        value={mac}
        onChange={(e) => setMac(e.target.value)}
      />
      <button onClick={handleApply}>Apply</button>
    </div>
  );
}