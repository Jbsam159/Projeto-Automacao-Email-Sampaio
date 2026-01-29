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
  msg.set_content("Seu cliente de email não suporta HTML.")
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