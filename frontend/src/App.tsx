import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";

// Pages
import { UploadBoletos } from "./pages/UploadBoletos";
import HistoricoBoletos from "./pages/HistoricoBoletos";
import Login from "./pages/Login";

// Components
import { Footer } from "./components/Footer";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <div className="app-layout">
      <BrowserRouter>

        <nav className="navbar">
          <h2 className="navbar-logo">📄 Automação de Boletos</h2>

          <div className="navbar-links">
            <Link className="nav-link" to="/">Upload</Link>
            <Link className="nav-link" to="/historico">Histórico</Link>
          </div>
        </nav>

        <div className="app-content">
          <Routes>

            {/* Login (rota pública) */}
            <Route path="/login" element={<Login />} />

            {/* Upload (rota protegida) */}
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <UploadBoletos />
                </PrivateRoute>
              }
            />

            {/* Histórico (rota protegida) */}
            <Route
              path="/historico"
              element={
                <PrivateRoute>
                  <HistoricoBoletos />
                </PrivateRoute>
              }
            />

            {/* Rota inválida */}
            <Route path="*" element={<Navigate to="/" />} />

          </Routes>
        </div>

        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
