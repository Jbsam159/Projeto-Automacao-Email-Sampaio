from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.file_service import generate_sha256
import os
from app.services.boleto_extractor import extract_text, extract_boleto_data
from fastapi.encoders import jsonable_encoder
from app.core.database import get_db
from app.services.boleto_service import criar_boletos

from app.services.email_service import enviar_email
from app.services.email_templates import template_cobranca_boleto

router = APIRouter()

UPLOAD_DIR = "uploads/boletos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-boletos")
async def upload_boletos(
    email_cliente: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    saved_files = []

    for file in files:
        file_bytes = await file.read()
        file_hash = generate_sha256(file_bytes)
        file_path = f"uploads/boletos/{file_hash}.pdf"

        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(file_bytes)

        text = extract_text(file_path)
        boleto_data = extract_boleto_data(text)

        dados_boleto = {
            "hash_pdf": file_hash,
            "nome_cliente": boleto_data["nome_cliente"],
            "valor": boleto_data["valor"],
            "data_vencimento": boleto_data["data_vencimento"],
            "linha_digitavel": boleto_data["linha_digitavel"],
            "arquivo_path": file_path,
            "email_cliente": email_cliente
        }

        try:
            boleto = criar_boletos(db, dados_boleto)

        except ValueError:
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "duplicado",
            })
            continue

        try:
            corpo_email = template_cobranca_boleto({
                "nome_cliente": boleto.nome_cliente,
                "valor": boleto.valor,
                "data_vencimento": boleto.data_vencimento,
                "linha_digitavel": boleto.linha_digitavel,
            })

            enviar_email(
                para=email_cliente,
                assunto="Boleto em Aberto",
                corpo=corpo_email,
                anexo_path=boleto.arquivo_path
            )

            status = "salvo_enviado"

        except Exception as e:
            # Email falhou, mas boleto está salvo
            status = "salvo_nao_enviado"
            print(f"Erro ao enviar email: {e}")


        saved_files.append({
            "filename": file.filename,
            "hash": file_hash,
            "status": status,
        })

    return {
        "message": "Processamento concluído",
        "files": saved_files
    }
