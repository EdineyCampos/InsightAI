
from inteligencia_planilhas import identificar_colunas


def test_identificar_colunas_conhecidas():
    colunas = [
        "Produto",
        "Quantidade",
        "Preco_Unitario",
        "ID_Venda"
    ]

    resultado = identificar_colunas(colunas)

    assert resultado["identificadas"]["Produto"] == "Produto"
    assert resultado["identificadas"]["Quantidade"] == "Quantidade"
    assert resultado["identificadas"]["Preco"] == "Preco_Unitario"
    assert resultado["identificadas"]["ID_Venda"] == "ID_Venda"

def test_identificar_colunas_ambiguas():
    colunas = [
        "Produto",
        "Quantidade",
        "Preco_Unitario",
        "ID_Venda",
        "Numero do Pedido",
        "Codigo da Venda"
    ]

    resultado = identificar_colunas(colunas)

    assert "ID_Venda" not in resultado["identificadas"]

    assert "ID_Venda" in resultado["ambiguas"]
    assert "Numero do Pedido" in resultado["ambiguas"]
    assert "Codigo da Venda" in resultado["ambiguas"]

def test_identificar_colunas_desconhecidas():
    colunas = [
        "Produto",
        "Quantidade",
        "Preco_Unitario",
        "Observacoes_Internas"
    ]

    resultado = identificar_colunas(colunas)

    assert "Observacoes_Internas" in resultado["desconhecidas"]

    assert "Observacoes_Internas" not in resultado["ambiguas"]

    assert "Observacoes_Internas" not in resultado["identificadas"].values()

