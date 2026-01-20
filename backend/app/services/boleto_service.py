from sqlalchemy.orm import Session
from app.models.boleto import Boleto

# Função de criar boleto
def criar_boleto(db: Session, dados: dict) -> Boleto:
    boleto = Boleto(**dados)
    db.add(boleto)
    db.commit()
    db.refresh(boleto)
    return boleto
