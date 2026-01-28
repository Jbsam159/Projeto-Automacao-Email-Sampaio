from app.services.email_templates import template_cobranca_boleto

dados_boleto = {
  "nome_cliente": "João da Silva",
  "valor": "567.40",
  "data_vencimento": "16/01/2026",
  "linha_digitavel": "34191.09008 03431.206550 70235.350009 1 13280000056740"
}

email = template_cobranca_boleto(dados_boleto)

print("=== TEMPLATE GERADO ===")
print(email)
