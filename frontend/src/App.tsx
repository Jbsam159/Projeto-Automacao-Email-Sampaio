import { BrowserRouter, Routes, Route, Navigate, Link} from "react-router-dom";

// Importando Pages
import { UploadBoletos } from "./pages/UploadBoletos"
import HistoricoBoletos from "./pages/HistoricoBoletos"
import { Footer } from "./components/Footer";

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
            {/* Tela principal */}
            <Route path="/" element={<UploadBoletos />} />

            {/* Histórico */}
            <Route path="/historico" element={<HistoricoBoletos />} />

            {/* Rota inválida → redireciona */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>

        </div>

        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
