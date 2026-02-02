from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# Criando Model da entidade Emails_Enviados
class EmailEnviado(Base):
  __tablename__ = "emails_enviados"

  id = Column(Integer, primary_key=True, index=True)
  boleto_id = Column(Integer, ForeignKey("boletos.id"), nullable=False)
  email_destinatario = Column(String, nullable=False)
  assunto = Column(String, nullable=False)
  data_envio = Column(DateTime, default=datetime.utcnow)
  status = Column(String, nullable=False)
  erro = Column(Text, nullable=True)

  boleto = relationship("Boleto", back_populates="emails_enviados")
  criado_em = Column(DateTime(timezone=True), server_default=func.now())

