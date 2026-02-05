# Importando FASTAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

from app.core.config import settings

import os

# Importando Upload
from app.api import upload
from app.api import boletos

# Importando scheduler
from app.core.scheduler import start_scheduler

# Importando Modelos
from app.models import Boleto
from app.models import EmailEnviado

app = FastAPI(
  title="Automação de Cobrança via Email",
  description="API para upload e processamento de boletos vencidos",
  version="1.0"
)

@app.on_event("startup")
def startup_event():
  Base.metadata.create_all(bind=engine)
  start_scheduler()

app.add_middleware(
  CORSMiddleware,
  allow_origins=[settings.frontend_url, "https://envio.sampaiodf.com.br/"],  # frontend
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(boletos.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=int(os.environ.get("PORT",8000))
  )