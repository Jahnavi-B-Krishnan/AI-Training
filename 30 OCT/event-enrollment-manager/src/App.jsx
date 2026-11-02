
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Events from "./pages/Events";
import Registrations from "./pages/Registrations";

function App() {
  return (
    <div>
      <Navbar />

      <main className="container">
        <Routes>
          <Route path="/" element={<Events />} />

          <Route
            path="/registrations"
            element={<Registrations />}
          />

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
