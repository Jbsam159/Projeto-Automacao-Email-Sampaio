from datetime import datetime

def template_cobranca_boleto(boletos: list, logo_cid: str) -> str:
    itens = ""

    for boleto in boletos:
        itens += f"""
        <tr>
            <td>{boleto.nome_cliente}</td>
            <td>R$ {boleto.valor}</td>
            <td>{boleto.data_vencimento}</td>
            <td>{boleto.linha_digitavel}</td>
        </tr>
        """

    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; ">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="cid:{logo_cid}" width="180" style="margin-bottom:20px;" />
            </div>

            <p>Olá,</p>

            <p>Identificamos os seguintes boletos em aberto:</p>

            <table border="1" cellpadding="8" cellspacing="0" width="100%">
                <tr>
                    <th>Cliente</th>
                    <th>Valor</th>
                    <th>Vencimento</th>
                    <th>Linha Digitável</th>
                </tr>
                {itens}
            </table>

            <p>Segue anexo boleto atualizado.</p>
            
            <p style="margin-top: 20px;">
                Caso o pagamento já tenha sido realizado, por favor desconsidere este email.
            </p>

            <p>
                Atenciosamente<br><strong>Sampaio Distribuidora</strong><br>Osmar/Odmar
            </p>
        </body>
    </html>
    """



