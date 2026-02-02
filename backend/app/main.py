# Importando FASTAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando Upload
from app.api import upload
from app.api import boletos

# Importando scheduler
from app.core.scheduler import start_scheduler

app = FastAPI(
  title="Automação de Cobrança via Email",
  description="API para upload e processamento de boletos vencidos",
  version="1.0"
)

@app.on_event("startup")
def startup_event():
  start_scheduler()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],  # frontend
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(boletos.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}