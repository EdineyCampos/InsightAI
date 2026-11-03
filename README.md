
# 📊 InsightAI — Automação Inteligente de Relatórios

O InsightAI é uma aplicação desenvolvida em Python para automatizar a análise de dados de vendas, gerar indicadores de desempenho, visualizar resultados e produzir recomendações utilizando Inteligência Artificial.

## 🚀 Funcionalidades

- Upload de planilhas Excel (.xlsx)
- Cálculo automático de faturamento
- Indicadores de desempenho de vendas
- Identificação do produto com maior faturamento
- Gráficos interativos com Plotly
- Análise de dados utilizando Google Gemini
- Geração de insights e recomendações de negócio
- Exportação de relatórios em Excel
- Download de análises geradas por IA em Markdown

## 🛠️ Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL
- Google Gemini API
- Git e GitHub (versionamento e hospedagem do código)

## ⚙️ Como executar

1. Clone o repositório:

   git clone URL_DO_REPOSITORIO

2. Entre na pasta do projeto.

3. Instale as dependências:

   python -m pip install -r requirements.txt

4. Configure sua chave GEMINI_API_KEY no arquivo
   .streamlit/secrets.toml.

5. Execute a aplicação:

   python -m streamlit run interface.py

## 📁 Dados de exemplo

O repositório inclui o arquivo `vendas.xlsx`, com dados fictícios para demonstrar as funcionalidades do sistema.

## 🎯 Objetivo

Demonstrar competências práticas em programação Python, análise de dados, automação de processos, visualização de informações e integração com modelos de Inteligência Artificial.

## 🔒 Segurança

As credenciais de API são armazenadas separadamente do código-fonte. O arquivo `.streamlit/secrets.toml` está incluído no `.gitignore` para evitar sua publicação acidental.

## 📌 Sobre o projeto

O InsightAI é um projeto pessoal de portfólio, desenvolvido para fins educacionais e de demonstração de competências técnicas.

Não possui finalidade comercial nem vínculo ou afiliação com empresas ou organizações que eventualmente utilizem nomes semelhantes.

## 🚧 Status

Projeto em desenvolvimento.
