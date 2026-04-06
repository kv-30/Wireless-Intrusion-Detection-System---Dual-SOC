import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { StoreProvider } from "./app/store";
import "./styles/theme.css";
import "./styles/dashboard-cyber.css";


const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <StoreProvider>
      <App />
    </StoreProvider>
  </React.StrictMode>
);