import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def clean_nome_cliente(nome: str) -> str:
    # Remove tudo após CNPJ ou CPF
    nome = re.split(r"\b(CNPJ|CPF)\b", nome, flags=re.IGNORECASE)[0]

    # Remove números no final (caso não tenha escrito CNPJ/CPF)
    nome = re.split(r"\d{2,}", nome)[0]

    return nome.strip()

def normalize_valor(valor_str: str) -> Decimal | None:
    try:
        valor_str = valor_str.replace(".", "").replace(",", ".")
        valor = Decimal(valor_str)
        return valor.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, AttributeError):
        return None


# =========================
# EXTRAÇÃO DE TEXTO
# =========================

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


# =========================
# EXTRAÇÃO DE DADOS
# =========================

def extract_nome_cliente(text: str) -> str | None:
    """
    Heurística:
    - Procura 'Pagador' ou 'Sacado'
    - Retorna a primeira linha válida após isso
    """
    linhas = [l.strip() for l in text.splitlines() if l.strip()]

    INVALID_NOME_KEYWORDS = [
        "autenticação",
        "compensação",
        "ficha",
        "corte",
        "banco",
        "código",
        "local de pagamento",
        "vencimento",
    ]

    for i, linha in enumerate(linhas):
        linha_lower = linha.lower()

        # Caso 1: Pagador ou Sacado na mesma linha
        if linha_lower.startswith(("pagador:", "sacado:")):
            nome = linha.split(":", 1)[1].strip()
            if nome and not any(k in nome.lower() for k in INVALID_NOME_KEYWORDS):
                return clean_nome_cliente(nome)


        # Caso 2: Pagador ou Sacado como título
        if linha_lower in ("pagador", "sacado"):
            for prox in linhas[i + 1:i + 6]:
                prox_lower = prox.lower()

                if any(k in prox_lower for k in INVALID_NOME_KEYWORDS):
                    continue

                if len(prox) > 5 and any(c.isalpha() for c in prox):
                    return clean_nome_cliente(prox)


    return None


def extract_boleto_data(text: str) -> dict:
    data = {}

    # Nome do cliente
    nome = extract_nome_cliente(text)
    if nome:
        data["nome_cliente"] = nome

    # Valor (ex: R$ 567.40)
    valor_match = re.search(r"R\$[\s]*([\d.,]+)", text)
    if valor_match:
        data["valor"] = normalize_valor(valor_match.group(1))

    # Data de vencimento (Vencimento ou VCTO)
    venc_match = re.search(
        r"(?:Vencimento|VCTO)[^\d]*(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE
    )
    if venc_match:
        data["data_vencimento"] = venc_match.group(1)

    # Linha digitável
    linha_match = re.search(
        r"\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14}",
        text
    )
    if linha_match:
        data["linha_digitavel"] = linha_match.group(0)

    return data
