# Importando FASTAPI
from fastapi import FastAPI

app = FastAPI(
  title="Automação de Cobrança via Email",
  description="API para upload e processamento de boletos vencidos",
  version="1.0"
)

@app.get("/health")
def health_check():
  return {"status": "ok"}