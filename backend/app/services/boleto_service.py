from sqlalchemy.orm import Session
from app.models.boleto import Boleto

def boleto_ja_existe(db: Session, hash_pdf: str) -> bool:
  return db.query(Boleto).filter(Boleto.hash_pdf == hash_pdf).first() is not None

# Função de criar boleto
def criar_boletos(db: Session, dados: dict) -> Boleto:
  if boleto_ja_existe(db, dados["hash_pdf"]):
    raise ValueError("Boleto Duplicado!")
  
  boleto = Boleto(**dados)
  
  db.add(boleto)
  db.commit()
  db.refresh(boleto)
  return boleto