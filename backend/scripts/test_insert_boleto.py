from app.core.database import SessionLocal
from app.services.boleto_service import criar_boleto

db = SessionLocal()

boleto = criar_boleto(db, {
    "hash_pdf": "hash_teste",
    "nome_cliente": "Cliente Teste",
    "valor": 123.45,
    "data_vencimento": "2026-01-16",
    "linha_digitavel": "123456789",
    "status": "pendente",
    "arquivo_path": "uploads/teste.pdf"
})

print(boleto.id)
