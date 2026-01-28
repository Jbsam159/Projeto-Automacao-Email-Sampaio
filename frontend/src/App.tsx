import { BrowserRouter, Routes, Route, Navigate, Link} from "react-router-dom";

// Importando Pages
import { UploadBoletos } from "./pages/UploadBoletos"
import HistoricoBoletos from "./pages/HistoricoBoletos"

function App() {
  return (
    <BrowserRouter>

      <Link to="/">Upload</Link>
      <Link to="/historico">Histórico</Link>

      <Routes>
        {/* Tela principal */}
        <Route path="/" element={<UploadBoletos />} />

        {/* Histórico */}
        <Route path="/historico" element={<HistoricoBoletos />} />

        {/* Rota inválida → redireciona */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
