import { useState } from "react";
import { api } from "../api/api";

import { Alert } from "../components/Alert/Alert";
import { Loading } from "../components/Loading/Loading";
import { EmptyState } from "../components/EmptyState/EmptyState";
import { Card } from "../components/Card/Card";

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
      setResultados([]);

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
      console.error(err);
      setErro("Erro ao enviar boletos. Verifique o backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title="Upload de Boletos">
      {/* ERRO */}
      {erro && <Alert type="error" message={erro} />}

      {/* FORM */}
      <div className="form-group">
        <label htmlFor="email">Email do cliente</label>
        <input
          id="email"
          type="email"
          placeholder="cliente@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="form-group">
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
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        Enviar boletos
      </button>

      {/* LOADING */}
      {loading && <Loading text="Processando boletos..." />}

      {/* RESULTADOS */}
      {!loading && resultados.length === 0 && (
        <EmptyState message="Nenhum boleto processado ainda." />
      )}

      {!loading && resultados.length > 0 && (
        <div className="resultados">
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
    </Card>
  );
}
