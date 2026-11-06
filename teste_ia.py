
import streamlit as st

from inteligencia_planilhas import sugerir_colunas_com_ia

colunas_teste = [
    "Item Comercializado",
    "Qtd. Saída",
    "Valor Unitário",
    "Receita",
    "Data da Venda"
]

print("Iniciando teste de reconhecimento com Gemini...")

resultado = sugerir_colunas_com_ia(
    colunas=colunas_teste,
    api_key=st.secrets["GEMINI_API_KEY"]
)

print("\nSugestões do Gemini:")

for campo, coluna in resultado.items():
    print(f"{campo}: {coluna}")
