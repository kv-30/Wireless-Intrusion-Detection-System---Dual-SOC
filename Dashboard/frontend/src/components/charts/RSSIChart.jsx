
import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export function RSSIChart({ data = [] }) {
  const labels = data.map((d, idx) => {
    const ts = d.timestamp || d._time;
    if (!ts) return `${idx + 1}`;
    return new Date(ts).toLocaleTimeString();
  });
  const chartData = {
    labels,
    datasets: [
      {
        label: "Avg RSSI",
        data: data.map(d => Number(d.avg_rssi ?? 0)),
        borderColor: "rgb(54, 162, 235)",
        backgroundColor: "rgba(54, 162, 235, 0.2)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: { color: "#bfdbfe" },
      },
      title: { display: true, text: "RSSI Over Time", color: "#dbeafe" },
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
        beginAtZero: false,
        ticks: { color: "#94a3b8" },
        grid: { color: "rgba(59, 130, 246, 0.12)" },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}