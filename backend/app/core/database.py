# Importando libs importantes
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from typing import Generator


# Carregando as variáveis de ambiente
load_dotenv()

# Pegando valor da URL do BD pelo env
DATABASE_URL = os.getenv("DATABASE_URL")

# Criando engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

Base = declarative_base()

def get_db() -> Generator:
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()