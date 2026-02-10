import { useState } from "react";
import { api } from "../api/api";

import { Alert } from "../components/Alert/Alert";
import { Loading } from "../components/Loading/Loading";
import { EmptyState } from "../components/EmptyState/EmptyState";
import { Card } from "../components/Card/Card";

import EmailSelect from "../components/EmailSelect";
import { useEmailHistory } from "../hooks/useEmailHistory";

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
  const { emails, addEmail } = useEmailHistory();

  function validarFormulario() {
    if (!email) {
      setErro("Informe o email do cliente.");
      return false;
    }

    if (files.length === 0) {
      setErro("Selecione ao menos um arquivo PDF.");
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
      addEmail(email)
    } catch (err) {
      console.error(err);
      setErro("Erro ao enviar boletos. Tente novamente.");
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
        <EmailSelect
        value={email}
        onChange={setEmail}
        options={emails}
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

          <div className="result-list">
            {resultados.map((item, index) => (
              <div key={index} className={`result-card ${item.status}`}>
                <div className="result-header">
                  <span className="result-icon">
                    {item.status === "salvo_enviado" && "✅"}
                    {item.status === "duplicado" && "⚠️"}
                    {item.status === "arquivo_invalido" && "❌"}
                    {item.status === "dados_incompletos" && "❌"}
                  </span>

                  <strong className="result-status">
                    {item.status.replace("_", " ").toUpperCase()}
                  </strong>
                </div>

                <p className="result-file">
                  📄 {item.filename}
                </p>

                <p className="result-description">
                  {item.status === "duplicado" && "Este boleto já havia sido processado."}
                  {item.status === "salvo" && "Boleto processado com sucesso."}
                  {item.status === "arquivo_invalido" && "Arquivo inválido (não é PDF)."}
                  {item.status === "dados_incompletos" && "Dados importantes estão faltando."}
                </p>
              </div>
            ))}
        </div>
          
        </div>
      )}
    </Card>
  );
}