import smtplib
from email.message import EmailMessage
import os
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
  corpo: str,
  anexo_path: str | None = None

) -> None:
  
  print("HOST:", SMTP_HOST)
  print("PORT:", SMTP_PORT)

  msg = EmailMessage()
  msg["From"] = EMAIL_FROM
  msg["To"] = para
  msg["Subject"] = assunto
  msg.set_content(corpo)

  # Anexando boleto PDF
  if anexo_path:
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