# 📋 Issues — MVP Automação de Cobrança via Upload de PDFs

Este documento descreve as **issues do MVP** do sistema de automação de cobrança baseado no upload de boletos vencidos em PDF.

---

## 🎯 Visão Geral do Fluxo do MVP

```text
PDF do boleto (Itaú)
        ↓
Upload manual no sistema
        ↓
Extração de texto do PDF
        ↓
Parsing (regex) dos dados do boleto
        ↓
Validações e regras de negócio
        ↓
Persistência no banco
        ↓
Envio de email de cobrança
        ↓
Registro do envio
```

---

## 🧱 EPIC 1 — Setup do Projeto

### 🟢 Issue 1.1 — Inicializar backend com FastAPI
**Descrição**
- Criar estrutura base do projeto
- Configurar ambiente virtual
- Criar endpoint `/health`

**Critérios de aceite**
- Projeto sobe com `uvicorn`
- Endpoint `/health` retorna HTTP 200

---

### 🟢 Issue 1.2 — Configurar banco de dados
**Descrição**
- Configurar PostgreSQL
- Criar conexão com SQLAlchemy
- Criar migrations iniciais

**Critérios de aceite**
- Conexão com banco funcionando
- Migração aplicada com sucesso

---

## 📦 EPIC 2 — Upload e Processamento de PDFs

### 🟢 Issue 2.1 — Endpoint de upload de boletos (PDF)
**Descrição**
- Criar endpoint `/upload-boletos`
- Aceitar múltiplos arquivos PDF
- Validar tipo e tamanho do arquivo

**Critérios de aceite**
- PDFs válidos são aceitos
- Arquivos inválidos são rejeitados

---

### 🟢 Issue 2.2 — Armazenamento dos PDFs
**Descrição**
- Salvar PDFs localmente ou em storage
- Gerar hash SHA-256 do arquivo

**Critérios de aceite**
- PDF salvo corretamente
- Hash único gerado por arquivo

---

### 🟢 Issue 2.3 — Leitura e extração de dados do boleto
**Descrição**
- Ler texto do PDF
- Extrair automaticamente:
  - Nome do cliente
  - Valor do boleto
  - Data de vencimento
  - Linha digitável

**Critérios de aceite**
- Dados extraídos corretamente a partir de PDFs reais

---

## 🧾 EPIC 3 — Persistência e Regras de Negócio

### 🟢 Issue 3.1 — Modelagem da entidade Boleto
**Descrição**
- Criar tabela `boletos`
- Criar model ORM correspondente

**Critérios de aceite**
- Boleto salvo no banco com sucesso
- Campos obrigatórios validados

---

### 🟢 Issue 3.2 — Prevenção de duplicidade de boletos
**Descrição**
- Verificar existência de boleto pelo hash do PDF
- Bloquear cadastro duplicado

**Critérios de aceite**
- Upload duplicado não cria novo registro

---

### 🟢 Issue 3.3 — Identificação de boleto vencido
**Descrição**
- Comparar data de vencimento com a data atual
- Marcar boleto como `VENCIDO`

**Critérios de aceite**
- Boletos vencidos identificados corretamente

---

## 📧 EPIC 4 — Envio de Email de Cobrança

### 🟢 Issue 4.1 — Configurar serviço de email (SMTP)
**Descrição**
- Criar serviço de envio de emails
- Configurar variáveis de ambiente (host, porta, usuário, senha)

**Critérios de aceite**
- Email enviado com sucesso via SMTP

---

### 🟢 Issue 4.2 — Criar template de email de cobrança
**Descrição**
- Criar template simples e profissional
- Inserir dados do boleto dinamicamente

**Critérios de aceite**
- Email claro, objetivo e legível

---

### 🟢 Issue 4.3 — Envio de email com anexo (PDF)
**Descrição**
- Anexar PDF do boleto ao email
- Enviar automaticamente após upload e validação

**Critérios de aceite**
- Email enviado com o PDF correto em anexo

---

### 🟢 Issue 4.4 — Registro de emails enviados
**Descrição**
- Criar tabela `emails_enviados`
- Registrar data de envio e boleto associado

**Critérios de aceite**
- Histórico de emails salvo corretamente

---

## 🧪 EPIC 5 — Qualidade e Segurança

### 🟢 Issue 5.1 — Validações e tratamento de erros
**Descrição**
- Tratar PDF inválido
- Tratar erro de extração de dados
- Tratar falha no envio de email

**Critérios de aceite**
- Sistema não quebra
- Retornos de erro claros e controlados

---

### 🟢 Issue 5.2 — Logs básicos do sistema
**Descrição**
- Criar logs para:
  - Upload de PDFs
  - Extração de dados
  - Envio de emails

**Critérios de aceite**
- Logs visíveis no console ou arquivo

---

### 🟢 Issue 6.1 — Setup do projeto frontend

**Descrição**

Criar o projeto base do frontend com Vite + React + TypeScript.

**Tarefas**

- Criar projeto com Vite
- Limpar arquivos padrão
- Criar estrutura inicial de pastas
- Configurar Axios com baseURL do backend
- Testar comunicação com backend (ping simples)

**Critérios de aceite**

- Projeto sobe com npm run dev
- Estrutura organizada
- Axios configurado e funcionando

---

### 🟢 Issue 6.2 — Tela de Upload de Boletos

**Descrição**

Criar a tela principal para upload de boletos PDF.

**Funcionalidades**

- Campo de email do cliente
- Upload de um ou vários arquivos PDF
- Validação básica (PDF obrigatório)
- Botão de envio
- Loading durante processamento

**Integração**
- ``POST /upload-boletos``

**Critérios de aceite**

- Upload funcional
- Requisição enviada corretamente
- Interface responsiva

---

### 🟢 Issue 6.3 — Exibição de status do processamento

**Descrição**

Exibir o resultado retornado pelo backend após o upload.

**Funcionalidades**

- Lista de arquivos processados
- Status exibido de forma clara:
        - salvo_enviado
        - salvo_nao_enviado
        - duplicado
        - erro_extracao
        - dados_incompletos
- Feedback visual (cores, ícones simples)

**Critérios de aceite**

- Usuário entende claramente o que aconteceu com cada boleto
- Interface limpa e legível

---

### 🟢 Issue 6.4 — Tela de histórico de boletos

**Descrição**

Criar tela de leitura do histórico de boletos cadastrados.

**Funcionalidades**

- Listar boletos vindos do backend
- Exibir:
        - Nome do cliente
        - Valor
        - Data de vencimento
        - Status
        - Email do cliente
- Atualização automática ao entrar na tela

**Integração**
- `GET /boletos`

**Critérios de aceite**

- Dados exibidos corretamente
- Interface organizada
- Sem edição (somente leitura)

---

### 🟢 Issue 6.5 — Polimento visual e UX

**Descrição**

Aprimorar a experiência do usuário.

**Funcionalidades**

- Mensagens de erro amigáveis
- Feedback visual consistente
- Layout alinhado e espaçado
- Estados vazios (“Nenhum boleto encontrado”)

**Critérios de aceite**

- Interface profissional
- Boa usabilidade
- Projeto apresentável para portfólio

---

## 📘 EPIC 7 — Documentação

### 🟢 Issue 7.1 — Criar README do MVP
**Descrição**
- Documentar:
  - Objetivo do projeto
  - Tecnologias utilizadas
  - Como rodar o projeto
  - Fluxo do sistema

**Critérios de aceite**
- Qualquer desenvolvedor consegue rodar o projeto apenas com o README

---

## 🏁 Ordem Recomendada de Execução

1. EPIC 1 — Setup do Projeto  
2. EPIC 2 — Upload e Processamento de PDFs  
3. EPIC 3 — Persistência e Regras de Negócio  
4. EPIC 4 — Envio de Email  
5. EPIC 5 — Qualidade e Segurança
6. EPIC 6 — Documentação 
7. EPIC 7 — Documentação  

---

## 🏷️ Labels sugeridas
- `feature`
- `backend`
- `email`
- `pdf`
- `database`
- `docs`
- `bug`

