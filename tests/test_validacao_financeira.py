
import pandas as pd
import pytest

from validacao_financeira import validar_dados_financeiros


@pytest.mark.parametrize(
    "coluna, valor, problema",
    [
        ("Quantidade", None, "Valor ausente ou inválido"),
        ("Preco", None, "Valor ausente ou inválido"),
        ("Quantidade", -5, "Valor negativo"),
        ("Preco", -120, "Valor negativo"),
    ]
)
def test_identificar_problema_financeiro(coluna, valor, problema):
    dados = pd.DataFrame({
        coluna: [10, valor]
    })

    resultado = validar_dados_financeiros(dados, [coluna])

    assert resultado == [{
        "Linha do Excel": 3,
        "Coluna": coluna,
        "Problema": problema
    }]


def test_dados_financeiros_validos():
    dados = pd.DataFrame({
        "Quantidade": [2, 5, 10],
        "Preco": [3500, 900, 250]
    })

    resultado = validar_dados_financeiros(
        dados,
        ["Quantidade", "Preco"]
    )

    assert resultado == []


def test_multiplos_problemas_financeiros():
    dados = pd.DataFrame({
        "Quantidade": [2, None, 10],
        "Preco": [3500, 900, -250]
    })

    resultado = validar_dados_financeiros(
        dados,
        ["Quantidade", "Preco"]
    )

    assert len(resultado) == 2

    assert {
        "Linha do Excel": 3,
        "Coluna": "Quantidade",
        "Problema": "Valor ausente ou inválido"
    } in resultado

    assert {
        "Linha do Excel": 4,
        "Coluna": "Preco",
        "Problema": "Valor negativo"
    } in resultado
