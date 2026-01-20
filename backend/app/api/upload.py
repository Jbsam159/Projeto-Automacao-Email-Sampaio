from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import generate_sha256
import os
from app.services.boleto_extractor import extract_text, extract_boleto_data
from fastapi.encoders import jsonable_encoder
from app.services.boleto_service import criar_boleto
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

UPLOAD_DIR = "uploads/boletos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-boletos")
async def upload_boletos(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    saved_files = []

    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Apenas PDFs são permitidos")

        file_bytes = await file.read()

        file_hash = generate_sha256(file_bytes)
        file_path = os.path.join(UPLOAD_DIR, f"{file_hash}.pdf")

        # Evita salvar duplicado
        if os.path.exists(file_path):
            saved_files.append({
                "filename": file.filename,
                "status": "duplicado",
                "hash": file_hash
            })
            continue

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        text = extract_text(file_path)

        print("====================================")
        print("TEXTO EXTRAÍDO DO PDF:")
        print(text[:1000])  # imprime só os primeiros 1000 caracteres
        print("====================================")

        boleto_data = extract_boleto_data(text)

        valor = boleto_data.get("valor")

        boleto_data["valor"] = (
            format(valor, ".2f") if valor is not None else None
        )

        dados_boleto = {
            "hash_pdf": file_hash,
            "nome_cliente": boleto_data.get("nome_cliente"),
            "valor": boleto_data.get("valor"),
            "data_vencimento": boleto_data.get("data_vencimento"),
            "linha_digitavel": boleto_data.get("linha_digitavel"),
            "status": "pendente",
            "arquivo_path": file_path,
        }

        # 🔹 Persistência (issue 3.1 / 3.2)
        criar_boleto(db, dados_boleto)

        saved_files.append({
            "filename": file.filename,
            "status": "salvo",
            "hash": file_hash,
            "dados_extraidos": boleto_data
        })

    return {
        "message": "Processamento concluído",
        "files": saved_files
    }
