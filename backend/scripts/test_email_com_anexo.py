from app.services.email_service import enviar_email

enviar_email(
  para="osmarsam@terra.com.br",
  assunto="Teste boleto com anexo",
  corpo="Segue boleto em anexo.",
  anexo_path="uploads/boletos/teste.pdf"
)

print("✅ Email com anexo enviado")
