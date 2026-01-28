from datetime import datetime

def template_cobranca_boleto(dados: dict) -> str:
    """
    Gera o corpo do email de cobrança com base nos dados do boleto
    """

    nome = dados.get("nome_cliente", "Cliente")
    valor = dados.get("valor", "0.00")
    vencimento = dados.get("data_vencimento", "")
    linha_digitavel = dados.get("linha_digitavel", "")

    return f"""
Olá, {nome}

Esperamos que esteja tudo bem.

Identificamos que o boleto abaixo encontra-se em aberto:

📄 Dados do boleto:
• Valor: R$ {valor}
• Vencimento: {vencimento}
• Linha digitável:
{linha_digitavel}

Caso o pagamento já tenha sido realizado, por favor desconsidere este email.

Se precisar de qualquer ajuda, estamos à disposição.

Atenciosamente,
Equipe Financeira
"""
