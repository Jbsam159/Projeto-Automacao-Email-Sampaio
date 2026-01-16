from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import generate_sha256
import os

router = APIRouter()

UPLOAD_DIR = "uploads/boletos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-boletos")
async def upload_boletos(files: list[UploadFile] = File(...)):
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

        saved_files.append({
            "filename": file.filename,
            "status": "salvo",
            "hash": file_hash
        })

    return {
        "message": "Processamento concluído",
        "files": saved_files
    }
