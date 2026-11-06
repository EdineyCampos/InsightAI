# 📊 InsightAI — Automação Inteligente de Relatórios

O **InsightAI** é uma aplicação web desenvolvida em Python para automatizar a análise de planilhas de vendas, identificar inconsistências financeiras, visualizar indicadores de desempenho e gerar recomendações de negócio utilizando Inteligência Artificial.

O projeto foi desenvolvido pensando especialmente em pequenos comerciantes que precisam transformar seus dados de vendas em informações claras e úteis para a tomada de decisões, sem exigir conhecimentos avançados em programação ou análise de dados.

## 🌐 Experimente o InsightAI Online

**🚀 [Acessar o InsightAI](https://ediney-insightai.streamlit.app/)**

A aplicação pode ser utilizada diretamente pelo navegador, sem necessidade de instalar Python ou outras ferramentas.

Basta enviar uma planilha Excel com dados de vendas para explorar os indicadores, gráficos, validações e relatórios disponíveis.

## 🚀 Funcionalidades

### 📂 Importação e tratamento de dados

- Upload de planilhas Excel (`.xlsx`).
- Reconhecimento e padronização de colunas.
- Identificação de dados ausentes, inválidos ou negativos.
- Identificação de registros duplicados.
- Opção de desconsiderar vendas duplicadas dos cálculos.
- Orientações para correção de inconsistências encontradas.

### 📊 Análise e indicadores de vendas

- Cálculo automático do faturamento total.
- Apuração da quantidade de unidades vendidas.
- Cálculo da receita média por unidade.
- Identificação dos produtos com maior faturamento.
- Visualização de resultados por meio de gráficos interativos com Plotly.

### 🔎 Validação financeira

- Conferência de divergências entre os valores informados na planilha e os valores calculados.
- Identificação das vendas que apresentam inconsistências financeiras.
- Apresentação das diferenças encontradas para facilitar sua conferência.
- Exportação de relatório Excel específico com as divergências identificadas.

### 🤖 Análise com Inteligência Artificial

- Integração com a API do Google Gemini.
- Geração de análises e recomendações de negócio baseadas nos dados processados.
- Apresentação dos resultados em linguagem acessível.
- Exportação da análise produzida pela IA em PDF.

### 📥 Exportação de relatórios

- Download de relatório Excel com os dados de vendas.
- Planilha de resumo com indicadores e gráfico.
- Relatório específico para conferência de divergências financeiras.
- Download da análise da Inteligência Artificial em PDF.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| **Python** | Desenvolvimento e automação |
| **Pandas** | Processamento, tratamento e análise de dados |
| **Streamlit** | Interface web interativa |
| **Plotly** | Visualização de dados e gráficos |
| **OpenPyXL** | Geração e formatação de relatórios Excel |
| **Google Gemini API** | Análises e recomendações com IA |
| **ReportLab** | Geração de documentos PDF |
| **Pytest** | Testes automatizados |
| **Git e GitHub** | Versionamento e repositório do projeto |
| **Streamlit Community Cloud** | Hospedagem da aplicação online |

## ⚙️ Como executar localmente

**1. Clone o repositório:**

```bash
git clone https://github.com/EdineyCampos/InsightAI.git
```

**2. Acesse a pasta do projeto:**

```bash
cd InsightAI
```

**3. Instale as dependências:**

```bash
python -m pip install -r requirements.txt
```

**4. Configure a chave da API do Gemini.**

Crie o arquivo `.streamlit/secrets.toml` e adicione:

```toml
GEMINI_API_KEY = "SUA_CHAVE_AQUI"
```

**5. Execute o aplicativo:**

```bash
python -m streamlit run interface.py
```

**6.** Abra o endereço local informado no terminal.

> **Alternativa:** para utilizar a aplicação sem instalação, acesse [InsightAI Online](https://ediney-insightai.streamlit.app/).

## 📁 Dados de exemplo

O projeto utiliza planilhas de vendas para demonstrar o processamento de dados, a identificação de inconsistências, o cálculo de indicadores e a geração de relatórios.

Os testes também utilizam dados fictícios para verificar diferentes situações de validação financeira.

## 🧪 Testes automatizados

O InsightAI possui testes automatizados com **Pytest**, voltados à validação das regras de processamento e conferência financeira.

Para executar os testes:

```bash
python -m pytest tests/ -q -p no:cacheprovider
```

Os testes ajudam a verificar o comportamento das funcionalidades e a reduzir o risco de regressões durante a evolução do projeto.

## 🎯 Objetivo do projeto

O InsightAI foi desenvolvido para aplicar conhecimentos de programação, análise de dados, automação e Inteligência Artificial na resolução de um problema prático.

O projeto demonstra competências em:

- Desenvolvimento de aplicações Python.
- Tratamento e validação de dados.
- Análise de indicadores de negócios.
- Automação de relatórios.
- Visualização de dados.
- Integração com APIs de Inteligência Artificial.
- Testes automatizados.
- Versionamento e publicação de aplicações web.

## 🔒 Segurança

As credenciais da API são mantidas separadas do código-fonte.

Na execução local, a chave do Gemini é armazenada em `.streamlit/secrets.toml`, que deve permanecer fora do versionamento por meio do `.gitignore`.

Na hospedagem online, as credenciais devem ser configuradas no gerenciamento de *Secrets* do Streamlit Community Cloud.

**Nenhuma chave de API deve ser incluída diretamente no código ou publicada no repositório.**

## 📌 Sobre o projeto

O InsightAI é um projeto pessoal de portfólio, desenvolvido para fins educacionais e demonstração de competências técnicas em desenvolvimento de software, dados e Inteligência Artificial.

Não possui vínculo ou afiliação com empresas ou organizações que eventualmente utilizem nomes semelhantes.

## ✅ Status

**Versão funcional publicada online.**

O InsightAI está disponível para acesso e demonstração no Streamlit Community Cloud.

**🔗 [Experimentar o InsightAI](https://ediney-insightai.streamlit.app/)**