import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";

const Login = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [modal, setModal] = useState<null | "success" | "error">(null);
  const [modalMessage, setModalMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);

    try {
      await login(email, password);
      setModal("success");
      setModalMessage("Login realizado com sucesso!");

      setTimeout(() => {
        navigate("/", {replace: true});
      }, 1200)

    } catch {
      setModal("error");
      setModalMessage("Email ou senha inválidos.");
    } finally{
      setLoading(false)
    }
  }

  return (
    
    <div className="login-container">

      <form className="login-card" onSubmit={handleSubmit}>

        <h2 className="login-title">Tela de Login</h2>
        <p className="login-subtitle">Acesse sua conta para continuar</p>

        <input
          type="text"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "⏳ Entrando..." : "Entrar"}
        </button>

      </form>

      {/* MODAL */}
      {modal && (
        <div className="modal-overlay">
          <div className={`modal ${modal}`}>
            <p>{modalMessage}</p>
            {modal === "error" && (
              <button onClick={() => setModal(null)}>Fechar</button>
            )}
          </div>
        </div>
      )}

    </div>
  );
};

export default Login;
