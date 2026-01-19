# Importando libs importantes
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric
from sqlalchemy.sql import func
from app.core.database import Base

# Criando modelo do Boleto
class Boleto(Base):
  __tablename__ = "Boletos"

  id = Column(Integer, primary_key=True, index=True)

  hash_pdf = Column(String, nullable=False, unique=True, index=True)
  nome_cliente = Column(String, nullable=False)
  valor = Column(Numeric(15,2), nullable=False)

  data_vencimento = Column(Date, nullable=False)
  linha_digitavel = Column(String, nullable=False)

  status = Column(String, nullable=False, default="pendente")

  criado_em = Column(DateTime(timezone=True), server_default=func.now())