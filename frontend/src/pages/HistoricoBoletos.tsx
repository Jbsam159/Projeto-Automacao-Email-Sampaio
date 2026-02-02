import { useEffect, useState } from "react";
import { api } from "../api/api";

type Boleto = {
  id: number;
  nome_cliente: string;
  valor: number;
  data_vencimento: string;
  status: string;
  email_cliente: string;
  data_envio: string;
};

export default function HistoricoBoletos() {
  const [boletos, setBoletos] = useState<Boleto[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/boletos")
      .then((res) => setBoletos(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Carregando histórico...</p>;

return (
  <div className="page-container">
    <h2 className="page-title">Histórico de Boletos</h2>

    {boletos.length === 0 ? (
      <p className="empty-state">Nenhum boleto encontrado.</p>
    ) : (
      <div className="table-wrapper">
        <table className="boletos-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Email</th>
              <th>Valor</th>
              <th>Vencimento</th>
              <th>Status</th>
              <th>Enviado em</th>
            </tr>
          </thead>
          <tbody>
            {boletos.map((b) => (
              
              <tr key={b.id}>
                <td>{b.nome_cliente}</td>
                <td>{b.email_cliente}</td>
                <td>R$ {b.valor.toFixed(2)}</td>
                <td>{new Date(b.data_vencimento).toLocaleDateString("pt-BR")}</td>
                <td>
                  <span className={`status-badge ${b.status}`}>
                    {b.status.replace("_", " ")}
                  </span>
                </td>
                <td>
                  {new Date(b.data_envio).toLocaleDateString("pt-BR")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);
}
