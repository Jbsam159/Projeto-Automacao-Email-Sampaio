# Importando FASTAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando Upload
from app.api import upload

app = FastAPI(
  title="Automação de Cobrança via Email",
  description="API para upload e processamento de boletos vencidos",
  version="1.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],  # frontend
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(upload.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}