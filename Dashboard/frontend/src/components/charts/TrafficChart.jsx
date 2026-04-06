// src/components/charts/TrafficChart.jsx
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export function TrafficChart({ data = [], baseline = 0 }) {
  const labels = data.map((d, idx) => {
    const ts = d.timestamp || d._time;
    if (!ts) return `${idx + 1}`;
    return new Date(ts).toLocaleTimeString();
  });
  const trafficData = data.map(d => Number(d.traffic ?? 0));
  const baselineData = data.map(() => Number(baseline ?? 0));

  const chartData = {
    labels,
    datasets: [
      {
        label: "Traffic",
        data: trafficData,
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
      },
      {
        label: "Baseline",
        data: baselineData,
        borderColor: "rgba(255,99,132,0.5)",
        borderDash: [5, 5],
        pointRadius: 0,
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
      title: { display: true, text: "Traffic Over Time", color: "#dbeafe" },
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
        ticks: { color: "#94a3b8" },
        grid: { color: "rgba(59, 130, 246, 0.12)" },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}