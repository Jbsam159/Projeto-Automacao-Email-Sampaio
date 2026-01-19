# Importando funções e Modelo do Boleto
from app.core.database import engine, Base
from app.models.boleto import Boleto

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
