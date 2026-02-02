# Libs importadas
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.boleto import Boleto
from app.models.email_enviado import EmailEnviado

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.boleto import Boleto
from app.models.email_enviado import EmailEnviado

def limpar_boletos_expirados(db: Session):
  limite = datetime.utcnow() - timedelta(hours=24)

  boletos_expirados = db.query(Boleto).filter(
    Boleto.criado_em < limite
  ).all()

  for boleto in boletos_expirados:
    # apaga emails relacionados
    db.query(EmailEnviado).filter(
      EmailEnviado.boleto_id == boleto.id
    ).delete()

    # apaga o boleto
    db.delete(boleto)

  db.commit()

  return len(boletos_expirados)
