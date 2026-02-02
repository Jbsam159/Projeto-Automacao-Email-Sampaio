'''
import smtplib
from email.message import EmailMessage
import os
from email.utils import make_msgid
from app.core.config import (
  

  SMTP_HOST,
  SMTP_PORT,
  SMTP_USER,
  SMTP_PASSWORD,
  EMAIL_FROM

)

def enviar_email(
  
  para: str,
  assunto: str,
  corpo_html: str,
  anexos: list[str],
  logo_path: str | None = None,
  logo_cid: str | None = None

) -> None:
  
  print("HOST:", SMTP_HOST)
  print("PORT:", SMTP_PORT)

  msg = EmailMessage()
  msg["From"] = EMAIL_FROM
  msg["To"] = para
  msg["Subject"] = assunto

  # HTML do email
  msg.set_content("")
  msg.add_alternative(corpo_html, subtype="html")

  # 🔗 Logo inline (CID)
  if logo_path and logo_cid:
    with open(logo_path, "rb") as img:
      msg.get_payload()[1].add_related(
        img.read(),
        maintype="image",
        subtype="jpeg",
        cid=logo_cid
      )

  # Anexando boleto PDF
  for anexo_path in anexos: 
    with open(anexo_path, "rb") as f:
      file_data = f.read()
      file_name = os.path.basename(anexo_path)

    msg.add_attachment(
      file_data,
      maintype="application",
      subtype="pdf",
      filename=file_name
    )

  with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
'''

import base64
import requests
import os
from app.core.config import settings

RESEND_URL = "https://api.resend.com/emails"


def enviar_email(
    *,
    para: str,
    assunto: str,
    corpo_html: str,
    anexos: list[str] | None = None,
    logo_url: str | None = None,  # 👈 mudou
) -> None:

    headers = {
        "Authorization": f"Bearer {settings.resend_api_key}",
        "Content-Type": "application/json",
    }

    # Se tiver logo via URL, você injeta no HTML
    if logo_url:
        corpo_html = corpo_html.replace(
            "{{LOGO_URL}}",
            logo_url
        )

    attachments = []

    if anexos:
      for anexo_path in anexos:
          with open(anexo_path, "rb") as f:
              encoded = base64.b64encode(f.read()).decode()

          attachments.append({
              "filename": os.path.basename(anexo_path),
              "content": encoded,
              "content_type": "application/pdf"
          })

    payload = {
        "from": settings.email_from,
        "to": [para],
        "subject": assunto,
        "html": corpo_html,
        "attachments": attachments,
    }

    if attachments:
      payload["attachments"] = attachments

    response = requests.post(
        RESEND_URL,
        headers=headers,
        json=payload,
        timeout=10,
    )

    print("STATUS:", response.status_code)
    print("RESPOSTA:", response.text)

    if response.status_code >= 400:
        raise RuntimeError(
            f"Erro Resend: {response.status_code} - {response.text}"
        )
