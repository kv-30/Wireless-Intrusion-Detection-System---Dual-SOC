import React from "react";

const DashboardLayout = ({ children }) => {
  return (
    <div className="dashboard cyber-dashboard">
      {/* Main content */}
      {children}

      {/* Floating Action Button */}
      <button
        className="cyber-fab"
        title="Quick Action"
      >
        ⚡
      </button>
    </div>
  );
};

export default DashboardLayout;