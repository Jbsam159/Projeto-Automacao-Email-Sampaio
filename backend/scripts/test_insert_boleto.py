from app.core.database import SessionLocal
from app.services.boleto_service import criar_boletos

db = SessionLocal()

dados_boleto = {
    "hash_pdf": "hash_teste_3",
    "nome_cliente": "Cliente Teste",
    "valor": 123.45,
    "data_vencimento": "2026-01-16",
    "linha_digitavel": "123456789",
    "status": "pendente",
    "arquivo_path": "uploads/teste.pdf"
}

# 1️⃣ Primeira inserção (deve funcionar)
boleto = criar_boletos(db, dados_boleto)
print("✅ Boleto criado com ID:", boleto.id)

db.close()
