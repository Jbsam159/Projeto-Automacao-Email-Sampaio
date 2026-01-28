import { useEffect } from "react";
import { api } from "../api/api";

function UploadBoletos() {
  useEffect(() => {
    api.get("/health")
      .then(() => console.log("Backend conectado ✅"))
      .catch(() => console.log("Erro ao conectar no backend ❌"));
  }, []);

  return (
    <div>
      <h1>Upload de Boletos</h1>
      <p>Veja o console do navegador</p>
    </div>
  );
}

export default UploadBoletos;
