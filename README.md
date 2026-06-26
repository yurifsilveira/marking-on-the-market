## Marcação a Mercado
![icon](https://badgen.net/badge/version/2.0.0#DDDDD?)

O projeto tem como objetivo desenvolver uma plataforma web para acompanhamento do mercado de renda fixa, com foco inicial em títulos públicos. A plataforma permitirá analisar a precificação dos títulos por meio da marcação a mercado, bem como acompanhar a evolução da curva de juros, fornecendo informações que auxiliem na identificação de oportunidades de compra e venda.


## Tecnologias
![Python](https://badgen.net/badge/Python/3.12/306998)
![Poetry](https://badgen.net/badge/Poetry/latest/000000)
![FastAPI](https://badgen.net/badge/FastAPI/%5E0.135.3/009688)
![SQLModel](https://badgen.net/badge/SQLModel/0.0.25/0B8043)
![SQLAlchemy](https://badgen.net/badge/SQLAlchemy/2.0.37/blue)
![psycopg](https://badgen.net/badge/psycopg/%5E3.3.3/grey)
![Flask](https://badgen.net/badge/Flask/3.1.3/000000)
![Flask-CORS](https://badgen.net/badge/Flask--CORS/6.0.2/f07e3b)
![redbird](https://badgen.net/badge/redbird/%5E0.7.0/2ECC71)
![pandas](https://badgen.net/badge/pandas/%5E2.2.3/150458)
![NumPy](https://badgen.net/badge/NumPy/%5E2.2.5/013243)
![Matplotlib](https://badgen.net/badge/Matplotlib/%5E3.10.1/11557C)
![requests](https://badgen.net/badge/requests/%5E2.32.3/6e1d8e)
![google-api-python-client](https://badgen.net/badge/google-api-python-client/%5E2.168.0/4285F4)
![google-auth-oauthlib](https://badgen.net/badge/google-auth-oauthlib/%5E1.2.2/4285F4)
![python-dotenv](https://badgen.net/badge/python--dotenv/%5E1.1.0/white)
![React](https://badgen.net/badge/React/19.2.4/61DAFB)
![ReactDOM](https://badgen.net/badge/ReactDOM/19.2.4/61DAFB)
![Vite](https://badgen.net/badge/Vite/%5E8.0.4/646CFF)
![ESLint](https://badgen.net/badge/ESLint/%5E9.39.4/4B32C3)
![@vitejs/plugin-react](https://badgen.net/badge/%40vitejs%2Fplugin-react/%5E6.0.1/646CFF)
![eslint-plugin-react-hooks](https://badgen.net/badge/eslint-plugin-react-hooks/%5E7.0.1/DD0031)
![eslint-plugin-react-refresh](https://badgen.net/badge/eslint-plugin-react-refresh/%5E0.5.2/61DAFB)
![globals](https://badgen.net/badge/globals/%5E17.4.0/AA77FF)


## Instalação e configuração

### Pré-requisitos

- Python 3.12
- Poetry
- Node.js 18+ e npm

### 1. Clonar o repositório

```bash
git clone https://github.com/yurifsilveira/marking-on-the-market.git
cd marking-on-the-market
```

### 2. Instalar dependências do backend

```bash
poetry install
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
URL_BANK=postgresql+psycopg://usuario:senha@localhost:5432/marking_market
URL_LEITURA_TITULOS=https://seu-endpoint/api/titulos
URL_CADASTRO_TITULOS=https://seu-endpoint/api/titulos
URL_ATUALIZAR_TITULOS=https://seu-endpoint/api/titulos
```

Essas variáveis são lidas pelo backend para conexão com o banco e integração com os endpoints de títulos.

### 4. Instalar dependências do frontend

```bash
cd frontend/marcacao-mercado
npm install
```

### 5. Executar o projeto

#### Backend

```bash
cd backend/db
poetry run uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend/marcacao-mercado
npm run dev
```

### 6. Atualização de dados (opcional)

Se for necessário carregar ou atualizar dados de títulos, execute:

```bash
cd backend/script
poetry run python __main__.py
```

## Status

In progress...