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
- Evitar cobrança duplicada do mesmo boleto

❌ O MVP não vai fazer:

- Login no banco
- Integração direta com o Itaú
- Geração de boletos
- Confirmação de pagamento
- Dashboard complexo
- Reenvio automático (fica para fase 2)

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

### 🎲 Modelagem de Dados (MVP

Este documento descreve a modelagem de dados do MVP considerando o processamento de **boletos vencidos em PDF**, utilizando como exemplo um boleto do cliente com razão social **RPD**.

🎯 Objetivo da Modelagem

Garantir que o sistema:

- Identifique unicamente cada boleto
- Extraia informações relevantes do PDF
- Evite cobranças duplicadas
- Permita o envio e controle de emails de cobrança

🧠 Conceito Central: Boleto

No contexto deste sistema, um **boleto** representa:

- Um documento financeiro oficial
- Uma cobrança em aberto
- Uma unidade independente de processamento

🧾 Entidade Principal: Boleto

### **Exemplo real**

- Cliente (Razão Social): **RPD**
- Situação: boleto vencido
- Origem: PDF baixado manualmente do Itaú

Estrutura da Entidade `Boleto`
| Campo | Tipo | Descrição |
|------|------|----------|
| id | UUID | Identificador único interno |
| razao_social | VARCHAR | Nome do cliente (ex: RPD) |
| email_cliente | VARCHAR | Email para cobrança |
| valor | DECIMAL(10,2) | Valor do boleto |
| data_vencimento | DATE | Data de vencimento |
| linha_digitavel | VARCHAR | Código do boleto |
| nosso_numero | VARCHAR | Identificador bancário (se existir) |
| status | ENUM | `VENCIDO` |
| hash_pdf | VARCHAR | Hash SHA-256 do PDF |
| caminho_pdf | VARCHAR | Local de armazenamento do PDF |
| data_importacao | TIMESTAMP | Data do upload |
| ultima_cobranca | TIMESTAMP | Data do último email enviado |

📧 Entidade de Apoio: Emails Enviados

**Finalidade**
Registrar cada tentativa de cobrança realizada pelo sistema.

📌 Estrutura da Entidade `emails_enviados`

| Campo      | Tipo      | Descrição                    |
| ---------- | --------- | ---------------------------- |
| id         | UUID      | Identificador único          |
| boleto_id  | UUID      | Referência ao boleto         |
| data_envio | TIMESTAMP | Quando o email foi enviado   |
| tipo       | VARCHAR   | Tipo de cobrança (ex: AVISO) |

🔄 Relacionamento entre entidades

```text
BOLETO 1 ---- N EMAILS_ENVIADOS
```

---

### ▶️ Como Iniciar o projeto

Dentro da pasta `backend/` execute o comando `.\venv\Scripts\activate` para iniciar o ambiente virtual e após isso execute o comando `uvicorn app.main:app --reload` para iniciar o servidor
