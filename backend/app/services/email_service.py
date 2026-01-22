import smtplib
from email.message import EmailMessage

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
  corpo: str

) -> None:
  
  print("HOST:", SMTP_HOST)
  print("PORT:", SMTP_PORT)
  msg = EmailMessage()
  msg["From"] = EMAIL_FROM
  msg["To"] = para
  msg["Subject"] = assunto
  msg.set_content(corpo)

  with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)