from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.services.file_service import generate_sha256
from app.services.boleto_extractor import extract_text, extract_boleto_data
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

        # ✅ Validação do tipo de arquivo
        if file.content_type != "application/pdf":
            saved_files.append({
                "filename": file.filename,
                "status": "arquivo_invalido"
            })
            continue

        file_bytes = await file.read()
        file_hash = generate_sha256(file_bytes)
        file_path = f"{UPLOAD_DIR}/{file_hash}.pdf"

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # ✅ PDF vazio
        if os.path.getsize(file_path) == 0:
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "pdf_vazio"
            })
            continue

        # ✅ Extração protegida
        try:
            text = extract_text(file_path)
            boleto_data = extract_boleto_data(text)
        except Exception:
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "erro_extracao"
            })
            continue

        # ✅ Validação dos dados
        campos_obrigatorios = [
            "nome_cliente",
            "valor",
            "data_vencimento",
            "linha_digitavel"
        ]

        if not all(boleto_data.get(campo) for campo in campos_obrigatorios):
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "dados_incompletos"
            })
            continue

        dados_boleto = {
            "hash_pdf": file_hash,
            "nome_cliente": boleto_data["nome_cliente"],
            "valor": boleto_data["valor"],
            "data_vencimento": boleto_data["data_vencimento"],
            "linha_digitavel": boleto_data["linha_digitavel"],
            "arquivo_path": file_path,
            "email_cliente": email_cliente
        }

        # ✅ Salvar boleto
        try:
            boleto = criar_boletos(db, dados_boleto)
        except ValueError:
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "duplicado"
            })
            continue

        # ✅ Envio de email isolado
        try:
            corpo_email = template_cobranca_boleto({
                "nome_cliente": boleto.nome_cliente,
                "valor": boleto.valor,
                "data_vencimento": boleto.data_vencimento,
                "linha_digitavel": boleto.linha_digitavel
            })

            enviar_email(
                para=email_cliente,
                assunto="Boleto em Aberto",
                corpo=corpo_email,
                anexo_path=boleto.arquivo_path
            )

            status = "salvo_enviado"

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            status = "salvo_nao_enviado"

        saved_files.append({
            "filename": file.filename,
            "hash": file_hash,
            "status": status
        })

    return {
        "message": "Processamento concluído",
        "files": saved_files
    }
