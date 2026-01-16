import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()

def extract_text_with_ocr(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image, lang="por")

    return text.strip()

def extract_text(pdf_path: str) -> str:
    text = extract_text_from_pdf(pdf_path)

    if not text or len(text) < 50:
        text = extract_text_with_ocr(pdf_path)

    return text

def extract_boleto_data(text: str) -> dict:
    data = {}

    # Nome do cliente (heurística simples)
    nome_match = re.search(r"Nome do Cliente[:\s]+(.+)", text, re.IGNORECASE)
    if nome_match:
        data["nome_cliente"] = nome_match.group(1).strip()

    # Valor
    valor_match = re.search(r"R\$[\s]*([\d.,]+)", text)
    if valor_match:
        data["valor"] = valor_match.group(1)

    # Data de vencimento
    venc_match = re.search(r"Vencimento[:\s]+(\d{2}/\d{2}/\d{4})", text)
    if venc_match:
        data["data_vencimento"] = venc_match.group(1)

    # Linha digitável (47 ou 48 dígitos)
    linha_match = re.search(r"(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})", text)
    if linha_match:
        data["linha_digitavel"] = linha_match.group(1)

    return data


