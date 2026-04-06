import React from "react";
import Dashboard from "./pages/Dashboard";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, message: error?.message || "Unknown error" };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Dashboard runtime error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 20, fontFamily: "Arial", background: "#0f172a", color: "#fff", minHeight: "100vh" }}>
          <h2>Dashboard failed to render</h2>
          <p>{this.state.message}</p>
          <p>Check browser console for stack trace.</p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  );
}