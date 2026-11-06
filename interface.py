
import streamlit as st
import plotly.express as px
from google import genai
from inteligencia_planilhas import identificar_colunas, reconhecer_colunas_hibrido
from validacao_financeira import validar_dados_financeiros



# Formatar valores no padrão brasileiro
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def converter_preco(valor):
    """Converte preços brasileiros e internacionais em números."""

    if pd.isna(valor):
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    texto = texto.replace("R$", "").replace(" ", "")

    if not texto:
        return None

    try:
        if "," in texto and "." in texto:
            if texto.rfind(",") > texto.rfind("."):
                texto = texto.replace(".", "").replace(",", ".")
            else:
                texto = texto.replace(",", "")

        elif "," in texto:
            texto = texto.replace(",", ".")

        return float(texto)

    except ValueError:
        return None

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
    
   
    # Limpar estados anteriores quando a planilha mudar
    if st.session_state.get("arquivo_anterior") != arquivo.getvalue():
        st.session_state["arquivo_anterior"] = arquivo.getvalue()
        st.session_state.pop("analise_ia", None)
        st.session_state.pop("sugestoes_colunas_ia", None)
        
        # Limpar a escolha do identificador ao trocar de planilha
        st.session_state.pop("identificador_transacao", None)
        
        # Reiniciar tratamento de duplicações ao trocar de planilha
        st.session_state.pop("tratar_duplicados", None)



        # Reiniciar a seleção das colunas
        for campo in ["Produto", "Quantidade", "Preco", "Faturamento"]:
            st.session_state.pop(f"mapeamento_{campo}", None)

    # Identificar colunas conhecidas
    reconhecimento = identificar_colunas(dados.columns.tolist())

    
    # Reconhecimento inteligente com Gemini
    if st.button("✨ Identificar colunas com IA"):
        with st.spinner("O Gemini está analisando as colunas..."):
            try:
                reconhecimento_ia = reconhecer_colunas_hibrido(
                    dados.columns.tolist(),
                    st.secrets["GEMINI_API_KEY"]
                )

                st.session_state["sugestoes_colunas_ia"] = (
                    reconhecimento_ia["colunas"]
                )
                
                # Reiniciar os seletores para aplicar as sugestões
                for campo in ["Produto", "Quantidade", "Preco", "Faturamento"]:
                    st.session_state.pop(
                        f"mapeamento_{campo}", None
                    )


                st.success("Análise das colunas concluída!")

            except Exception:
                st.error(
                    "Não foi possível consultar a IA. "
                    "Você pode selecionar as colunas manualmente."
                )

    st.subheader("🔎 Identificação das colunas")

    st.info(
        "Confira as colunas identificadas para garantir "
        "que os cálculos das vendas estejam corretos."
    )

    campos = ["Produto", "Quantidade", "Preco", "Faturamento"]
    opcoes = ["Selecione uma coluna"] + dados.columns.tolist()

    mapeamento = {}

    for campo in campos:
        
        # Priorizar o reconhecimento por regras.
        # Utilizar a IA para sugerir campos ainda não reconhecidos.
        sugestao = reconhecimento["identificadas"].get(campo)

        sugestoes_ia = st.session_state.get(
            "sugestoes_colunas_ia", {}
        )

        if sugestao is None:
            coluna_ia = sugestoes_ia.get(campo)

            if (
                coluna_ia in dados.columns
                and coluna_ia not in reconhecimento["ambiguas"]
            ):
                sugestao = coluna_ia

        indice = (
            opcoes.index(sugestao)
            if sugestao in opcoes
            else 0
        )

        mapeamento[campo] = st.selectbox(
            f"Coluna correspondente a {'Preço' if campo == 'Preco' else campo}",
            options=opcoes,
            index=indice,
            key=f"mapeamento_{campo}"
        )

    
    # Verificar os campos obrigatórios
    obrigatorios = ["Produto", "Quantidade"]

    if any(
        mapeamento[campo] == "Selecione uma coluna"
        for campo in obrigatorios
    ):
        st.warning(
            "Selecione as colunas de Produto e Quantidade."
        )
        st.stop()

    # Exigir preço unitário ou faturamento total
    tem_preco = mapeamento["Preco"] != "Selecione uma coluna"
    tem_faturamento = (
        mapeamento["Faturamento"] != "Selecione uma coluna"
    )

    if not tem_preco and not tem_faturamento:
        st.warning(
            "Selecione uma coluna de Preço ou Faturamento."
        )
        st.stop()


    
    # Verificar duplicações apenas entre colunas selecionadas
    colunas_selecionadas = [
        coluna
        for coluna in mapeamento.values()
        if coluna != "Selecione uma coluna"
    ]

    if len(set(colunas_selecionadas)) != len(colunas_selecionadas):
        st.error(
            "Uma mesma coluna não pode representar "
            "dois campos diferentes."
        )
        st.stop()


    # Padronizar nomes para os cálculos existentes
    
    dados = dados.rename(
        columns={
            coluna: campo
            for campo, coluna in mapeamento.items()
            if coluna != "Selecione uma coluna"
        }
    )



    st.success("Planilha carregada com sucesso!")

    st.subheader("Visualização dos dados")
    st.dataframe(dados, use_container_width=True)
    
    # Identificar valores ausentes na planilha
    valores_ausentes = dados.isna().sum()

    colunas_com_ausencias = valores_ausentes[
        valores_ausentes > 0
    ]

    if not colunas_com_ausencias.empty:
        st.warning(
            "Foram encontrados valores ausentes na planilha. "
            "Confira as colunas afetadas antes de continuar."
        )

        resumo_ausencias = colunas_com_ausencias.reset_index()
        resumo_ausencias.columns = [
            "Coluna",
            "Valores Ausentes"
        ]

        with st.expander("🔎 Visualizar valores ausentes"):
            st.dataframe(
                resumo_ausencias,
                use_container_width=True
            )
    else:
        st.success(
            "Nenhum valor ausente foi encontrado na planilha."
        )

    # Verificar registros completamente duplicados
    quantidade_duplicados = int(dados.duplicated().sum())

    if quantidade_duplicados > 0:
        st.warning(
            f"Foram encontrados {quantidade_duplicados} "
            "registros completamente duplicados na planilha."
        )

        registros_duplicados = dados[
            dados.duplicated(keep=False)
        ]

        with st.expander("🔎 Visualizar registros duplicados"):
            st.dataframe(
                registros_duplicados,
                use_container_width=True
            )
    else:
        st.success(
            "Nenhum registro completamente duplicado foi encontrado."
        )
        
    # Painel resumido de qualidade dos dados
    st.subheader("📊 Qualidade dos Dados")

    total_registros = len(dados)
    total_ausencias = int(valores_ausentes.sum())

    col_qual1, col_qual2, col_qual3 = st.columns(3)

    with col_qual1:
        st.metric(
            "Registros Analisados",
            total_registros
        )

    with col_qual2:
        st.metric(
            "Valores Ausentes",
            total_ausencias
        )

    with col_qual3:
        st.metric(
            "Registros Duplicados",
            quantidade_duplicados
        )


        
    # Permitir tratamento opcional de registros duplicados
    if quantidade_duplicados > 0:

        tratar_duplicados = st.checkbox(
            "Desconsiderar registros completamente duplicados nos cálculos",
            value=False,
            key="tratar_duplicados"
        )

        if tratar_duplicados:
            dados = dados.drop_duplicates().copy()

            st.info(
                f"{quantidade_duplicados} registros duplicados "
                "foram desconsiderados nesta análise. "
                "A planilha original não foi modificada."
            )




    # Validar dados necessários para os cálculos
    if dados.empty:
        st.error("A planilha está vazia.")
        st.stop()

   
    
    
    # Validar quantidade e os campos financeiros disponíveis
    colunas_numericas = ["Quantidade"]

    if tem_preco:
        colunas_numericas.append("Preco")

    if tem_faturamento:
        colunas_numericas.append("Faturamento")

    erros_financeiros = []
    detalhes_erros_financeiros = []

    for coluna in colunas_numericas:

        # Converter os valores para números
        if coluna in ["Preco", "Faturamento"]:
            dados[coluna] = dados[coluna].apply(converter_preco)
        else:
            dados[coluna] = pd.to_numeric(
                dados[coluna],
                errors="coerce"
            )

        nome_exibido = "Preço" if coluna == "Preco" else coluna

        # Verificar valores ausentes ou inválidos
        if dados[coluna].isna().any():
            erros_financeiros.append(
                f"A coluna {nome_exibido} contém valores vazios "
                "ou que não são números válidos."
            )
            
            # Registrar as linhas com valores ausentes ou inválidos
            linhas_invalidas = dados.index[
                dados[coluna].isna()
            ]

            for indice in linhas_invalidas:
                detalhes_erros_financeiros.append({
                    "Linha do Excel": int(indice) + 2,
                    "Coluna": nome_exibido,
                    "Problema": "Valor ausente ou inválido"
                })


        # Verificar valores negativos
        if (dados[coluna] < 0).any():
            erros_financeiros.append(
                f"A coluna {nome_exibido} contém valores negativos."
            )
            
            # Registrar as linhas com valores negativos
            linhas_negativas = dados.index[
                dados[coluna] < 0
            ]

            for indice in linhas_negativas:
                detalhes_erros_financeiros.append({
                    "Linha do Excel": int(indice) + 2,
                    "Coluna": nome_exibido,
                    "Problema": "Valor negativo"
                })
        
    # Comparar a validação antiga com o novo módulo
    problemas_modulo = validar_dados_financeiros(
        dados,
        colunas_numericas
    )

    # Padronizar e ordenar os resultados para comparação
    def normalizar_problemas(lista):
        return sorted(
            [
                {
                    "Linha do Excel": int(item["Linha do Excel"]),
                    "Coluna": {"Preco": "Preço"}.get(
                        str(item["Coluna"]).strip(),
                        str(item["Coluna"]).strip()
                    ),

                    "Problema": str(item["Problema"]).strip()
                }
                for item in lista
            ],
            key=lambda item: (
                item["Linha do Excel"],
                item["Coluna"],
                item["Problema"]
            )
        )

    problemas_antigos = normalizar_problemas(
        detalhes_erros_financeiros
    )

    problemas_novos = normalizar_problemas(
        problemas_modulo
    )

    # Exibir a comparação somente após validar todas as colunas
    
    
    if problemas_antigos == problemas_novos:
        st.success(
            "As duas validações financeiras apresentam resultados equivalentes."
        )
    else:
        st.warning(
            "Foram encontradas diferenças entre as validações financeiras."
        )

        with st.expander("🔎 Comparar resultados das validações"):
            st.write("Validação atual:")
            st.dataframe(
                pd.DataFrame(problemas_antigos),
                hide_index=True
            )

            st.write("Novo módulo:")
            st.dataframe(
                pd.DataFrame(problemas_novos),
                hide_index=True
            )
        

    # Mostrar todos os erros encontrados


    # Resumo da validação financeira
    total_problemas_financeiros = len(detalhes_erros_financeiros)

    st.subheader("💰 Qualidade dos Dados Financeiros")

    st.metric(
        "Problemas Financeiros Detectados",
        total_problemas_financeiros
    )
    
    # Informar o resultado da validação financeira
    if total_problemas_financeiros == 0:
        st.success(
            "Nenhum problema de validação financeira foi encontrado."
        )
    else:
        st.warning(
            f"Foram identificados {total_problemas_financeiros} "
            "problemas financeiros que precisam ser corrigidos."
        )


    if erros_financeiros:
        st.error(
            "Foram encontrados problemas nos dados financeiros:"
        )

        for erro in erros_financeiros:
            st.error(erro)
            
        # Mostrar localização dos problemas encontrados
        if detalhes_erros_financeiros:
            st.subheader("🔎 Localização dos Problemas")

            tabela_erros = pd.DataFrame(
                detalhes_erros_financeiros
            )

            st.dataframe(
                tabela_erros,
                use_container_width=True,
                hide_index=True
            )


        st.stop()


    if dados["Quantidade"].sum() == 0:
        st.warning(
            "Não existem unidades vendidas para calcular "
            "os indicadores desta planilha."
        )
        st.stop()


    # Calcular o faturamento automaticamente
    
    # Determinar a origem do faturamento
    if tem_faturamento:

        # Utilizar o valor total informado na planilha
        if tem_preco:
            faturamento_calculado = (
                dados["Quantidade"] * dados["Preco"]
            )

            divergencias = (
                (dados["Faturamento"] - faturamento_calculado)
                .abs() > 0.01
            )

            
            if divergencias.any():
                st.warning(
                    "Foram encontradas divergências entre "
                    "o faturamento informado e o calculado. "
                    "Os indicadores utilizarão o faturamento "
                    "informado na planilha."
                )

                # Resumo das divergências financeiras
                quantidade_divergencias = int(divergencias.sum())

                total_vendas = len(dados)

                diferenca_absoluta_total = (
                    dados.loc[divergencias, "Faturamento"]
                    - faturamento_calculado.loc[divergencias]
                ).abs().sum()
                
                # Separar divergências positivas e negativas
                diferencas_financeiras = (
                    dados.loc[divergencias, "Faturamento"]
                    - faturamento_calculado.loc[divergencias]
                )

                total_acima = (
                    diferencas_financeiras[
                        diferencas_financeiras > 0
                    ].sum()
                )

                total_abaixo = abs(
                    diferencas_financeiras[
                        diferencas_financeiras < 0
                    ].sum()
                )


                st.subheader("📊 Resumo das Divergências")

                col_div1, col_div2, col_div3, col_div4 = st.columns(4)

                with col_div1:
                    st.metric(
                        "Vendas com Divergências",
                        quantidade_divergencias
                    )

                with col_div2:
                    st.metric(
                        "Diferença Absoluta Total",
                        formatar_reais(diferenca_absoluta_total)
                    )

                with col_div3:
                    st.metric(
                        "Vendas Analisadas",
                        total_vendas
                    )
                
                # Percentual de vendas com divergências
                percentual_divergencias = (
                    quantidade_divergencias / total_vendas * 100
                    if total_vendas > 0
                    else 0
                )

                with col_div4:
                    st.metric(
                        "Percentual de Divergências",
                        f"{percentual_divergencias:.1f}%".replace(".", ",")
                    )

                    
                # Indicadores por direção da divergência
                col_acima, col_abaixo = st.columns(2)

                with col_acima:
                    st.metric(
                        "📈 Valores Acima do Esperado",
                        formatar_reais(total_acima)
                    )

                with col_abaixo:
                    st.metric(
                        "📉 Valores Abaixo do Esperado",
                        formatar_reais(total_abaixo)
                    )



                
                # Incluir identificação da venda quando disponível
                colunas_relatorio = [
                    "Produto", "Quantidade", "Preco", "Faturamento"
                ]

                
                # Reconhecer o identificador original da transação
                reconhecimento_id = identificar_colunas(
                    dados.columns.tolist()
                )

               
                coluna_id = reconhecimento_id["identificadas"].get(
                    "ID_Venda"
                )

                # Identificar possíveis colunas de transações ambíguas
                from inteligencia_planilhas import normalizar_nome, SINONIMOS

                nomes_id = {
                    normalizar_nome(nome)
                    for nome in SINONIMOS["ID_Venda"]
                }

                candidatas_id = [
                    coluna
                    for coluna in dados.columns
                    if normalizar_nome(coluna) in nomes_id
                ]

                if len(candidatas_id) > 1:
                    st.warning(
                        "Foram encontradas várias colunas que podem "
                        "identificar uma venda. Escolha a correta."
                    )

                    coluna_id = st.selectbox(
                        "Identificador da transação",
                        options=candidatas_id,
                        key="identificador_transacao"
                    )

                elif len(candidatas_id) == 1:
                    coluna_id = candidatas_id[0]

                if coluna_id is not None:
                    colunas_relatorio.insert(0, coluna_id)



                relatorio_divergencias = dados.loc[
                    divergencias,
                    colunas_relatorio
                ].copy()


                relatorio_divergencias["Valor Calculado"] = (
                    faturamento_calculado.loc[divergencias]
                )

                relatorio_divergencias["Diferença"] = (
                    relatorio_divergencias["Faturamento"]
                    - relatorio_divergencias["Valor Calculado"]
                )

                relatorio_divergencias = relatorio_divergencias.rename(
                    columns={
                        "Preco": "Preço Unitário",
                        "Faturamento": "Valor Informado"
                    }
                )

                st.subheader("⚠️ Vendas com Divergências")

                
                # Formatar valores monetários para exibição
                relatorio_exibicao = relatorio_divergencias.copy()

                colunas_monetarias = [
                    "Preço Unitário",
                    "Valor Informado",
                    "Valor Calculado",
                    "Diferença"
                ]

                for coluna in colunas_monetarias:
                    relatorio_exibicao[coluna] = (
                        relatorio_exibicao[coluna].apply(formatar_reais)
                    )


                st.dataframe(relatorio_exibicao,
                    use_container_width=True,
                    
                )


                # Exportar divergências em Excel
                from io import BytesIO

                arquivo_divergencias = BytesIO()

                
                with pd.ExcelWriter(
                    arquivo_divergencias,
                    engine="openpyxl"
                ) as writer:

                    relatorio_divergencias.to_excel(
                        writer,
                        index=False,
                        sheet_name="Divergencias"
                    )

                    planilha = writer.sheets["Divergencias"]

                    from openpyxl.styles import Font, PatternFill, Alignment
                    from openpyxl.utils import get_column_letter

                    # Destacar cabeçalhos
                    for celula in planilha[1]:
                        celula.font = Font(
                            bold=True,
                            color="FFFFFF"
                        )
                        celula.fill = PatternFill(
                            start_color="17365D",
                            end_color="17365D",
                            fill_type="solid"
                        )
                        celula.alignment = Alignment(
                            horizontal="center"
                        )

                    # Ajustar largura das colunas
                    for coluna in planilha.columns:
                        maior_tamanho = max(
                            len(str(celula.value))
                            if celula.value is not None else 0
                            for celula in coluna
                        )

                        letra = get_column_letter(coluna[0].column)

                        planilha.column_dimensions[letra].width = min(
                            maior_tamanho + 4,
                            40
                        )

                    # Formatar valores monetários
                    colunas_monetarias_excel = [
                        "Preço Unitário",
                        "Valor Informado",
                        "Valor Calculado",
                        "Diferença"
                    ]

                    for indice, celula in enumerate(planilha[1], start=1):
                        if celula.value in colunas_monetarias_excel:
                            for linha in range(2, planilha.max_row + 1):
                                planilha.cell(
                                    row=linha,
                                    column=indice
                                ).number_format = '"R$" #,##0.00'

                    # Manter cabeçalho visível ao rolar
                    planilha.freeze_panes = "A2"

                    # Habilitar filtros
                    planilha.auto_filter.ref = planilha.dimensions


                st.download_button(
                    label="📥 Baixar Relatório de Divergências",
                    data=arquivo_divergencias.getvalue(),
                    file_name="relatorio_divergencias.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    key="download_divergencias"
                )

    else:
        # Calcular quando não existe faturamento informado
        dados["Faturamento"] = (
            dados["Quantidade"] * dados["Preco"]
        )


    faturamento_total = dados["Faturamento"].sum()

    st.subheader("💰 Indicadores de Vendas")
   
    # Calcular indicadores
    unidades_vendidas = dados["Quantidade"].sum()
      
    receita_media = (
        faturamento_total / unidades_vendidas
        if unidades_vendidas > 0
        else 0
    )


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

   
    # Somar o faturamento de todas as vendas de cada produto
    faturamento_produtos = (
        dados.groupby("Produto", as_index=False)["Faturamento"]
        .sum()
        .sort_values("Faturamento", ascending=False)
    )

    # Criar gráfico com uma barra para cada produto
    grafico = px.bar(
        faturamento_produtos,
        x="Produto",
        y="Faturamento",
        title="Faturamento Total por Produto",
        text="Faturamento"
    )

    grafico.update_traces(
        texttemplate="R$ %{y:,.2f}",
        textposition="outside"
    )

    grafico.update_layout(
        xaxis_title="Produto",
        yaxis_title="Faturamento (R$)"
    )


    st.plotly_chart(grafico, use_container_width=True)

    # Identificar produto com maior faturamento
    indice_maior = faturamento_produtos["Faturamento"].idxmax()
    produto_destaque = faturamento_produtos.loc[indice_maior]

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

