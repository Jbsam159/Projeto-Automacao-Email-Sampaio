from app.core.database import SessionLocal
from app.models.boleto import Boleto
from app.services.email_service import enviar_email
from app.services.email_log_service import registrar_email_enviado

db = SessionLocal()

# Buscar um boleto existente no banco
boleto = db.query(Boleto).first()

if not boleto:
  print("❌ Nenhum boleto encontrado para teste")
  exit()

# Simula envio de email
enviar_email(
  para="jbsam159@gmail.com",
  assunto="Teste Registro Email",
  corpo="Email de teste",
  anexo_path=boleto.arquivo_path
)

# Registrar envio
registro = registrar_email_enviado(
  db=db,
  boleto_id=boleto.id,
  assunto="Assunto Teste de Registro",
  email_destinatario="teste@gmail.com",
  status="enviado"
)

print("✅ Registro criado com sucesso!")
print("ID:", registro.id)
print("Boleto ID:", registro.boleto_id)
print("Email:", registro.email_destinatario)

db.close()
