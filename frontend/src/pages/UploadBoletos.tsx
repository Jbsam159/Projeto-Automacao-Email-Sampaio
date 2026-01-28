import { useState } from "react";
import { api } from "../api/api";

type UploadResult = {
  filename: string;
  hash?: string;
  status: string;
};

export function UploadBoletos() {
  const [email, setEmail] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [resultados, setResultados] = useState<UploadResult[]>([]);
  const [erro, setErro] = useState<string | null>(null);

  function validarFormulario() {
  if (!email) {
    setErro("Informe o email do cliente.");
    return false;
  }

  if (files.length === 0) {
    setErro("Selecione ao menos um arquivo PDF.");
    return false;
  }

  const algumNaoPdf = files.some(
    (file) => file.type !== "application/pdf"
  );

  if (algumNaoPdf) {
    setErro("Todos os arquivos devem ser PDF.");
    return false;
  }

  setErro(null);
  return true;
}

async function handleSubmit() {
  if (!validarFormulario()) return;

  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

  try {
    setLoading(true);

    const response = await api.post(
      `/upload-boletos?email_cliente=${encodeURIComponent(email)}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    setResultados(response.data.files);
  } catch (err) {
    setErro("Erro ao enviar boletos. Verifique o backend.");
    console.error(err)
  } finally {
    setLoading(false);
  }
}


  return (
    <div>
      <h1>Upload de Boletos</h1>

      <label htmlFor="email">Email do cliente</label>
      <input
      id="email"
        type="email"
        placeholder="cliente@email.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required      
      />

      <label htmlFor="boletos">Boletos (PDF)</label>
      <input
      id="boletos"
        type="file"
        accept="application/pdf"
        multiple
        onChange={(e) => {
          if (!e.target.files) return;
          setFiles(Array.from(e.target.files));
        }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Enviando..." : "Enviar boletos"}
      </button>
      {erro && (
        <p style={{ color: "red", marginTop: 12 }}>
          {erro}
        </p>
      )}

      {resultados.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>Resultado do processamento</h3>
          <ul>
            {resultados.map((item, index) => (
              <li key={index}>
                <strong>{item.filename}</strong> — {item.status}
              </li>
            ))}
          </ul>
        </div>
      )}
      
    </div>
  );
}
