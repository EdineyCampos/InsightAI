
import ast
from pathlib import Path

import pandas as pd
import pytest


# Localizar a função sem executar o Streamlit
CAMINHO_INTERFACE = (
    Path(__file__).resolve().parents[1] / "interface.py"
)

codigo = CAMINHO_INTERFACE.read_text(encoding="utf-8")
arvore = ast.parse(codigo)

funcao = next(
    node
    for node in arvore.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "converter_preco"
)

modulo = ast.Module(body=[funcao], type_ignores=[])
ambiente = {"pd": pd}

exec(
    compile(modulo, str(CAMINHO_INTERFACE), "exec"),
    ambiente
)

converter_preco = ambiente["converter_preco"]


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        (3500, 3500.0),
        ("3500", 3500.0),
        ("3.500,00", 3500.0),
        ("R$ 3.500,00", 3500.0),
        ("125,50", 125.50),
        ("3,500.00", 3500.0),
        ("R$ 1.250,75", 1250.75),
    ]
)
def test_converter_valores_validos(entrada, esperado):
    resultado = converter_preco(entrada)

    assert resultado == pytest.approx(esperado)


@pytest.mark.parametrize(
    "entrada",
    [
        None,
        "",
        "   ",
        "valor invalido",
    ]
)
def test_converter_valores_invalidos(entrada):
    assert converter_preco(entrada) is None
