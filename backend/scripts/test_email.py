from app.services.email_service import enviar_email

enviar_email(
  para="jbsam159@gmail.com",
  assunto="Teste SMTP",
  corpo="Email enviado com sucesso 🎉"
)

print("✅ Email enviado com sucesso")
