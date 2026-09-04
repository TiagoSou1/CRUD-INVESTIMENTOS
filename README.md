# Investment Portfolio CRUD

A full-stack academic project for managing a small investment portfolio. A Flask API exposes Oracle database operations, while a responsive HTML/CSS/JavaScript interface handles registration, listing, deletion, broker reports, and portfolio totals.

## What it demonstrates

- REST-style endpoints with Flask
- Parameterized Oracle SQL queries
- Relational modeling with foreign keys and sequences
- Database triggers, a stored function, and a stored procedure
- Browser-side API consumption with JavaScript
- Environment-based configuration with no credentials committed to source control

## Features

- Register and list investments
- Delete an investment by identifier
- List configured brokers
- Filter investments by broker
- Calculate total portfolio value with `fn_patrimonio_total`
- Apply a 5% demonstration adjustment with `sp_valorizar_ativos`
- Check application configuration through `/api/health`

This is a learning project. It does not retrieve market prices, provide investment advice, or represent a production trading system.

## Architecture

```text
Browser interface
      │ fetch / JSON
      ▼
Flask API (`app.py`)
      │ python-oracledb
      ▼
Oracle Database
```

## Project structure

```text
CRUD-INVESTIMENTOS/
├── SQL/
│   ├── create.sql
│   └── inserts_exemplo.sql
├── templates/
│   └── index.html
├── .env.example
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

## Run locally

Requirements:

- Python 3.10+
- Oracle Database XE or another reachable Oracle instance
- Oracle credentials with permission to create and use the project objects

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Copy `.env.example` values into your shell environment. The application reads the variables directly; it does not load `.env` automatically.

PowerShell example:

```powershell
$env:ORACLE_USER = "your_user"
$env:ORACLE_PASSWORD = "your_password"
$env:ORACLE_DSN = "localhost:1521/XEPDB1"
```

Create the schema, then seed the illustrative records:

```text
SQL/create.sql
SQL/inserts_exemplo.sql
```

Start the server:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## API overview

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/health` | Check application and configuration status |
| `GET` | `/api/investimentos` | List investments |
| `POST` | `/api/investimentos` | Create an investment |
| `DELETE` | `/api/investimentos/{id}` | Delete an investment |
| `GET` | `/api/corretoras` | List brokers |
| `GET` | `/api/investimentos/corretora/{id}` | Filter by broker |
| `GET` | `/api/patrimonio-total` | Calculate total portfolio value |
| `POST` | `/api/valorizar-ativos` | Apply the demonstration procedure |

## Security and production gaps

- Never commit Oracle credentials; configure them through environment variables.
- The included CNPJ-like values are synthetic placeholders, not real customer data.
- Add authentication, authorization, CSRF protection, rate limits, input schemas, and automated tests before any production use.
- Restrict CORS to known origins in a deployed environment.
- Replace the fixed 5% procedure with a domain-valid process before real use.

## Author

Tiago Sousa Leite

Developed as an academic project for learning Python, APIs, and relational databases.

## Licensing

No software license has been granted for this repository.
