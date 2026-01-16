import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.core.config import MAX_FILE_SIZE_MB, ALLOWED_CONTENT_TYPES, UPLOAD_DIR

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-boletos")
async def upload_boletos(files: List[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        # Validação de tipo
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo inválido: {file.filename}"
            )

        # Validação de tamanho
        contents = await file.read()
        size_mb = len(contents) / (1024 * 1024)

        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande: {file.filename}"
            )

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        saved_files.append(file.filename)

    return {
        "message": "Upload realizado com sucesso",
        "files": saved_files
    }
