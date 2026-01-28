import { useEffect, useState } from "react";
import { api } from "../api/api";

type Boleto = {
  id: number;
  nome_cliente: string;
  valor: number;
  data_vencimento: string;
  status: string;
  email_cliente: string;
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
  <div>
    <h2>Histórico de Boletos</h2>

    <table>
      <thead>
        <tr>
          <th>Cliente</th>
          <th>Email</th>
          <th>Valor</th>
          <th>Vencimento</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {boletos.map((b) => (
          <tr key={b.id}>
            <td>{b.nome_cliente}</td>
            <td>{b.email_cliente}</td>
            <td>R$ {b.valor.toFixed(2)}</td>
            <td>{b.data_vencimento}</td>
            <td>{b.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  );
}
