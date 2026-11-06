
import pandas as pd


def validar_dados_financeiros(dados, colunas):
    """
    Identifica valores ausentes, inválidos e negativos
    nas colunas financeiras de uma planilha.
    """

    problemas = []

    for coluna in colunas:
        if coluna not in dados.columns:
            continue

        valores = pd.to_numeric(
            dados[coluna],
            errors="coerce"
        )

        for indice, valor in valores.items():
            if pd.isna(valor):
                tipo = "Valor ausente ou inválido"
            elif valor < 0:
                tipo = "Valor negativo"
            else:
                continue

            problemas.append({
                "Linha do Excel": int(indice) + 2,
                "Coluna": coluna,
                "Problema": tipo
            })

    return problemas
