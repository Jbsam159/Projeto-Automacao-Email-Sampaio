from app.core.database import SessionLocal
from app.models.boleto import Boleto

db = SessionLocal()

boleto = db.query(Boleto).first()

if not boleto:
  print("❌ Nenhum boleto encontrado")
  exit()

print(f"📄 Histórico de emails do boleto {boleto.id}:")

for email in boleto.emails_enviados:
  print(
    f"- {email.email_destinatario} | "
    f"{email.status} | "
    f"{email.data_envio}"
  )

db.close()
