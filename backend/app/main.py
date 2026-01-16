# Importando FASTAPI
from fastapi import FastAPI

# Importando Upload
from app.api import upload

app = FastAPI(
  title="Automação de Cobrança via Email",
  description="API para upload e processamento de boletos vencidos",
  version="1.0"
)

app.include_router(upload.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}