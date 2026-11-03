
import pandas as pd

# Ler a planilha
dados = pd.read_excel("vendas.xlsx")

# Calcular faturamento por produto
dados["Faturamento"] = dados["Quantidade"] * dados["Preco"]

# Calcular faturamento total
faturamento_total = dados["Faturamento"].sum()

# Mostrar resultados
print("=== InsightAI - Relatório de Vendas ===")
print(dados)
print(f"\nFaturamento total: R$ {faturamento_total:.2f}")

# Identificar o produto com maior faturamento
indice_maior = dados["Faturamento"].idxmax()
produto_destaque = dados.loc[indice_maior]

print("\n=== Destaque de Vendas ===")
print(f"Produto: {produto_destaque['Produto']}")
print(f"Faturamento: R$ {produto_destaque['Faturamento']:.2f}")

# Calcular indicadores de vendas
quantidade_total = dados["Quantidade"].sum()
total_produtos = len(dados)
ticket_medio = faturamento_total / quantidade_total

print("\n=== Indicadores de Vendas ===")
print(f"Unidades vendidas: {quantidade_total}")
print(f"Produtos diferentes: {total_produtos}")
print(f"Receita média por unidade: R$ {ticket_medio:.2f}")

# Gerar relatório automático em Excel
dados.to_excel("relatorio_vendas.xlsx", index=False)

print("\nRelatório Excel gerado com sucesso!")

import plotly.express as px

# Criar gráfico de faturamento por produto
grafico = px.bar(
    dados,
    x="Produto",
    y="Faturamento",
    title="InsightAI - Faturamento por Produto",
    text="Faturamento"
)

# Salvar gráfico interativo em HTML
grafico.write_html("grafico_vendas.html")

print("\nGráfico gerado com sucesso!")
