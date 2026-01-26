# Arquivo que registra o email

from sqlalchemy.orm import Session
from app.models.email_enviado import EmailEnviado

def registrar_email_enviado(
  db: Session,
  boleto_id: int,
  email_destinatario: str,
  assunto: str,
  status: str,
  erro: str | None = None
):
  registro = EmailEnviado(
    boleto_id=boleto_id,
    email_destinatario=email_destinatario,
    assunto=assunto,
    status=status,
    erro=erro
  )

  db.add(registro)
  db.commit()
  db.refresh(registro)
  
  return registro
