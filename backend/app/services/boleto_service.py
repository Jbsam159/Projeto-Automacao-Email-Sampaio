from sqlalchemy.orm import Session
from app.models.boleto import Boleto
from datetime import date, datetime


def boleto_ja_existe(db: Session, hash_pdf: str) -> bool:
  return db.query(Boleto).filter(Boleto.hash_pdf == hash_pdf).first() is not None

def verificar_vencimento(data_vencimento: date) -> str:
  hoje = date.today()

  if data_vencimento < hoje:
    return "vencido"
    
  return "pendente"

# Função de criar boleto
def criar_boletos(db: Session, dados: dict) -> Boleto:
    if boleto_ja_existe(db, dados["hash_pdf"]):
        raise ValueError("Boleto Duplicado!")

    # 🔎 Converte data se vier como string
    data_vencimento = dados.get("data_vencimento")
    if isinstance(data_vencimento, str):
        data_vencimento = datetime.strptime(
            data_vencimento, "%d/%m/%Y"
        ).date()

    # 🧠 Define status automaticamente
    dados["status"] = verificar_vencimento(data_vencimento)

    boleto = Boleto(**dados)

    db.add(boleto)
    db.commit()
    db.refresh(boleto)

    return boleto
