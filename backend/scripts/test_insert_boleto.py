from datetime import date
from app.core.database import SessionLocal
from app.models.boleto import Boleto

db = SessionLocal()

boleto = Boleto(
  hash_pdf="hash_teste_123",
  nome_cliente="João Victor",
  valor=150.75,
  data_vencimento=date(2026, 2, 10),
  linha_digitavel="12345.67890 12345.678901 1 12345678901234"
)

db.add(boleto)
db.commit()
db.refresh(boleto)

print("Boleto salvo com ID:", boleto.id)
db.close()
