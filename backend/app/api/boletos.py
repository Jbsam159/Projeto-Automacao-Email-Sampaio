from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.boleto import Boleto

router = APIRouter(prefix="/boletos", tags=["Boletos"])

@router.get("/")
def listar_boletos(db: Session = Depends(get_db)):
  boletos = db.query(Boleto).order_by(Boleto.criado_em.desc()).all()

  return [
    {
      "id": b.id,
      "nome_cliente": b.nome_cliente,
      "valor": float(b.valor),
      "data_vencimento": b.data_vencimento,
      "status": b.status,
      "email_cliente": b.email_cliente,
      "data_envio": (
        b.emails_enviados[-1].data_envio
        if b.emails_enviados
        else None
      )
    }
    for b in boletos
  ]
