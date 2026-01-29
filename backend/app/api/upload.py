from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os
from email.utils import make_msgid

from app.core.database import get_db
from app.services.file_service import generate_sha256
from app.services.boleto_extractor import extract_text, extract_boleto_data
from app.services.boleto_service import criar_boletos
from app.services.email_service import enviar_email
from app.services.email_templates import template_cobranca_boleto
from app.core.logger import get_logger

logo_cid = make_msgid()[1:-1]

logger = get_logger(__name__)
router = APIRouter()

UPLOAD_DIR = "uploads/boletos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-boletos")
async def upload_boletos(
    email_cliente: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    logger.info(
        f"Upload iniciado | email_cliente={email_cliente} | arquivos={len(files)}"
    )

    saved_files = []
    boletos_para_email = []
    anexos_email = []

    for file in files:
        logger.info(f"Iniciando processamento | arquivo={file.filename}")

        # ✅ Validação do tipo
        if file.content_type != "application/pdf":
            logger.warning(f"Arquivo inválido (não PDF) | arquivo={file.filename}")
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

        logger.info(f"PDF salvo | arquivo={file.filename} | hash={file_hash}")

        # ✅ PDF vazio
        if os.path.getsize(file_path) == 0:
            logger.warning(f"PDF vazio | arquivo={file.filename}")
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "pdf_vazio"
            })
            continue

        # ✅ Extração protegida
        try:
            logger.info(f"Iniciando extração | arquivo={file.filename}")
            text = extract_text(file_path)
            boleto_data = extract_boleto_data(text)

            if isinstance(boleto_data, list):
                if not boleto_data:
                    raise ValueError("Nenhum boleto extraído")

                if not isinstance(boleto_data[0], dict):
                    raise ValueError("Formato inválido de boleto extraído")

                boleto_data = boleto_data[0]

            if not isinstance(boleto_data, dict):
                raise ValueError("Dados extraídos não são um dicionário")

        except Exception as e:
            logger.error(
                f"Erro na extração | arquivo={file.filename} | tipo={type(boleto_data)} | | erro={e}"
            )
            saved_files.append({
                "filename": file.filename,
                "hash": file_hash,
                "status": "erro_extracao"
            })
            continue

        # ✅ Validação de campos
        campos_obrigatorios = [
            "nome_cliente",
            "valor",
            "data_vencimento",
            "linha_digitavel"
        ]

        if not all(boleto_data.get(campo) for campo in campos_obrigatorios):
            logger.warning(
                f"Dados incompletos | arquivo={file.filename}"
            )
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

        # ✅ Persistência
        try:
            boleto = criar_boletos(db, dados_boleto)
            logger.info(
                f"Boleto salvo | boleto_id={boleto.id} | hash={file_hash}"
            )

            boletos_para_email.append(boleto)
            anexos_email.append(boleto.arquivo_path)

            status = "salvo_enviado"

        except ValueError:
            logger.warning(
                f"Boleto duplicado | hash={file_hash}"
            )
            status = "duplicado"

        saved_files.append({
            "filename": file.filename,
            "hash": file_hash,
            "status": status
        })

    # ✉️ ENVIO ÚNICO DE EMAIL (FORA DO LOOP)
    if boletos_para_email:
        try:
            corpo_email = template_cobranca_boleto(boletos_para_email, logo_cid)

            enviar_email(
                para=email_cliente,
                assunto="Boletos em Aberto",
                corpo_html=corpo_email,
                anexos=anexos_email,
                logo_path="app/static/images/sampaio_logo.jpg",
                logo_cid=logo_cid
            )

            logger.info(
                f"Email enviado com sucesso | destinatario={email_cliente} | boletos={len(boletos_para_email)}"
            )

        except Exception as e:
            logger.error(
                f"Falha ao enviar email | destinatario={email_cliente} | erro={e}"
            )

    logger.info("Upload finalizado")

    return {
        "message": "Processamento concluído",
        "files": saved_files
    }
