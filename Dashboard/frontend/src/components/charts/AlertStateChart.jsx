
import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export function AlertStateChart({ data = [] }) {
  const labels = data.map((d, idx) => {
    const ts = d.timestamp || d._time;
    if (!ts) return `${idx + 1}`;
    return new Date(ts).toLocaleTimeString();
  });
  const chartData = {
    labels,
    datasets: [
      {
        label: "Alert State",
        data: data.map(d => (d.state === "ATTACK" ? 1 : 0)),
        backgroundColor: data.map(d => (d.state === "ATTACK" ? "#ef4444" : "#3b82f6")),
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: "Alert State Over Time", color: "#dbeafe" },
      tooltip: {
        backgroundColor: "#0f172a",
        borderColor: "#1d4ed8",
        borderWidth: 1,
        titleColor: "#e2e8f0",
        bodyColor: "#cbd5e1",
      },
    },
    scales: {
      x: {
        ticks: { color: "#94a3b8" },
        grid: { color: "rgba(59, 130, 246, 0.12)" },
      },
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1, color: "#94a3b8" },
        grid: { color: "rgba(59, 130, 246, 0.12)" },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}