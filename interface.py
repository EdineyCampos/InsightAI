
import streamlit as st
import plotly.express as px
from google import genai


# Formatar valores no padrão brasileiro
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Configurar a página
st.set_page_config(
    page_title="InsightAI",
    page_icon="📊",
    layout="wide"
)

# Título e apresentação
st.title("📊 InsightAI")
st.subheader("Automação Inteligente de Relatórios")

st.write(
    "Transforme planilhas em relatórios e análises "
    "de dados de forma automatizada."
)

st.success("Aplicação iniciada com sucesso!")

import pandas as pd

st.divider()

st.subheader("📁 Enviar planilha")

arquivo = st.file_uploader(
    "Selecione uma planilha Excel",
    type=["xlsx"]
)

if arquivo is not None:
    dados = pd.read_excel(arquivo)
    
    # Limpar análise anterior quando a planilha mudar
    if st.session_state.get("arquivo_anterior") != arquivo.getvalue():
        st.session_state["arquivo_anterior"] = arquivo.getvalue()
        st.session_state.pop("analise_ia", None)


    st.success("Planilha carregada com sucesso!")

    st.subheader("Visualização dos dados")
    st.dataframe(dados, use_container_width=True)

    # Calcular o faturamento automaticamente
    dados["Faturamento"] = dados["Quantidade"] * dados["Preco"]

    faturamento_total = dados["Faturamento"].sum()

    st.subheader("💰 Indicadores de Vendas")
   
    # Calcular indicadores
    unidades_vendidas = dados["Quantidade"].sum()
    receita_media = faturamento_total / unidades_vendidas

    # Organizar indicadores em três colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Faturamento Total",
            f"R$ {faturamento_total:,.2f}"
        )

    with col2:
        st.metric(
            "Unidades Vendidas",
            f"{unidades_vendidas}"
        )

    with col3:
        st.metric(
            "Receita Média por Unidade",
            f"R$ {receita_media:,.2f}"
        )

    # Criar gráfico de faturamento
    st.subheader("📊 Faturamento por Produto")

    grafico = px.bar(
        dados,
        x="Produto",
        y="Faturamento",
        title="Análise de Faturamento",
        text="Faturamento"
    )

    st.plotly_chart(grafico, use_container_width=True)

    # Identificar produto com maior faturamento
    indice_maior = dados["Faturamento"].idxmax()
    produto_destaque = dados.loc[indice_maior]

    st.subheader("🏆 Produto Destaque")

    st.success(
        f"O produto com maior faturamento foi "
        f"{produto_destaque['Produto']}, "
        f"com {formatar_reais(produto_destaque['Faturamento'])} em vendas."

    )

    # Preparar relatório Excel para download
    from io import BytesIO

    arquivo_excel = BytesIO()

    dados.to_excel(
        arquivo_excel,
        index=False,
        engine="openpyxl"
    )

    st.subheader("📥 Baixar Relatório")

    st.download_button(
        label="Baixar relatório Excel",
        data=arquivo_excel.getvalue(),
        file_name="relatorio_insightai.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Gerar análise inteligente com Gemini
    st.subheader("🤖 Análise Inteligente com IA")

    if st.button("Gerar análise com IA"):
        with st.spinner("Analisando os dados..."):
            cliente = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            resumo = dados[
                ["Produto", "Quantidade", "Faturamento"]
            ].to_string(index=False)

            prompt = f"""
            Você é um analista de dados especializado em vendas.

            Analise os seguintes dados:
            {resumo}

            Faturamento total: {formatar_reais(faturamento_total)}
            Unidades vendidas: {unidades_vendidas}

            Apresente:
            1. Um resumo dos resultados.
            2. Os produtos com maior e menor faturamento.
            3. Duas recomendações para o negócio.

            Responda em português, de forma objetiva.
            Não invente informações além dos dados fornecidos.
            Utilize o padrão brasileiro para valores monetários:
            R$ 1.200,00 em vez de R$ 1,200.00.
            Não utilize crases, blocos de código ou formatação
            de programação para apresentar valores monetários.
            Escreva os valores em reais como texto normal.
            
            Organize a resposta com títulos em Markdown.

            Utilize títulos no formato:
            ## 1. Resumo dos resultados
            ## 2. Produtos com maior e menor faturamento
            ## 3. Recomendações para o negócio

            Deixe uma linha em branco entre títulos e parágrafos.
            Utilize corretamente os acentos da língua portuguesa.
            Evite informações repetidas e mantenha a análise profissional.
            """

            
            try:
                resposta = cliente.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.session_state["analise_ia"] = resposta.text

            except Exception:
                st.error(
                    "Não foi possível gerar a análise neste momento. "
                    "Verifique sua conexão ou tente novamente mais tarde."
                )

    if "analise_ia" in st.session_state:
        
        texto_analise = st.session_state["analise_ia"]
        texto_analise = texto_analise.replace("R$", "R\\$")
        st.markdown(texto_analise)
        
        st.download_button(
            label="📥 Baixar análise da IA",
            data=st.session_state["analise_ia"],
            file_name="analise_insightai.md",
            mime="text/markdown"
        )

