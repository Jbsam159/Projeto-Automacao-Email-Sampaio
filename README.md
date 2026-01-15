# ⭐ Projeto Automação de Envio de Emails

### 📌 Sobre o Projeto
O projeto tem o principal objetivo de automatizar o envio de boletos para os clientes que ainda não pagaram, erradicando todo o processo manual de verificar qual cliente ainda não pagou, escrever o email e enviar.

---

### 🎯 Problema que Resolve
O projeto visa solucionar o problema da lerdeza de averiguar todo dia qual cliente ainda não pagou e escrever manualmente um email para o mesmo

---

### 🧩 Escopo do MVP
✅ O MVP vai fazer:
- Upload de 1 ou vários PDFs de boletos
- Extração automática de informações:
  - Nome do cliente
  - Valor do boleto
  - Data de vencimento
  - Linha digitável/código do boleto
- Cadastro automático do boleto no sistema(?)
- Identificação de boletos Vencidos
- Envio automático de email de cobranca
- Registro de:
  - Data de envio
  - Qual boleto foi cobrado
-  Evitar cobrança duplicada do mesmo boleto

❌ O MVP não vai fazer:
-  Login no banco
-  Integração direta com o Itaú
-  Geração de boletos
-  Confirmação de pagamento
-  Dashboard complexo
-  Reenvio automático (fica para fase 2)

---

### 💎 Fluxo do MVP

1. Usuário faz upload dos PDFs
2. Sistema lê os PDFs
3. Extrai os dados do boleto
4. Salva no banco (status: VENCIDO)
5. Verifica se já foi cobrado
6. Envia email ao cliente
7. Registra envio

---

### 🛠️ Stack Utilizada
Como stack utilizada, opto pelas seguintes tecnologias:

- Backend: Python + FastAPI + PostgreSQL
- Email: SMTP

---

