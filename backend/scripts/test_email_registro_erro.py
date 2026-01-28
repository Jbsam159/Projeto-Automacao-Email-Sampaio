from app.core.database import SessionLocal
from app.models.boleto import Boleto
from app.services.email_log_service import registrar_email_enviado

db = SessionLocal()

boleto = db.query(Boleto).first()

if not boleto:
  print("❌ Nenhum boleto encontrado para teste")
  exit()

# Simula erro de envio
registro = registrar_email_enviado(
  db=db,
  boleto_id=boleto.id,
  assunto="Assunto de Teste Inválido",
  email_destinatario="email_invalido@",
  status="erro"
)

print("✅ Registro de erro salvo corretamente")
print("Status:", registro.status)

db.close()
