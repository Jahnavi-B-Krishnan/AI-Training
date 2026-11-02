
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { RegistrationProvider } from "./context/RegistrationContext";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <RegistrationProvider>
        <App />
      </RegistrationProvider>
    </BrowserRouter>
  </React.StrictMode>
);
