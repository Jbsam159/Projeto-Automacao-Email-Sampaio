# Importando funções e Modelo do Boleto
from app.core.database import engine, Base
from app.models.boleto import Boleto
from app.models.email_enviado import EmailEnviado
from app.models.user import User

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")