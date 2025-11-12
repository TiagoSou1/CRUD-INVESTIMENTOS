A#  CRUD - Sistema de Carteira de Investimentos

Um sistema completo de **gestão de investimentos**, com **Flask (Python)** no back-end e **HTML + CSS + JavaScript** no front-end.  
Permite cadastrar, listar, excluir e valorizar ativos financeiros, além de gerar relatórios por corretora e calcular o patrimônio total.

---

##  Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask** — Framework web
- **Flask-CORS** — Para comunicação com o front-end
- **oracledb** — Conexão com banco de dados Oracle
- **Oracle SQL Developer / XE** — Banco de dados

### Frontend
- **HTML5 / CSS3 / JavaScript**
- Layout em estilo **terminal dark minimalista**
- Consumo de API com `fetch()`

---

##  Funcionalidades

 **CRUD completo de investimentos**
- Inserir novos ativos (ações, FIIs, cripto, renda fixa)
- Listar todos os investimentos com valores totais
- Excluir ativos individuais

 **Integração com banco Oracle**
- Tabelas: `Investimentos` e `Corretoras`
- Sequence: `seq_investimento`
- Function: `fn_patrimonio_total`
- Procedure: `sp_valorizar_ativos`

 **Relatórios e operações especiais**
- Relatório de investimentos por corretora
- Valorização automática de 5% (Procedure)
- Cálculo do patrimônio total (Function)

 **Interface moderna**
- Visual retrô em preto e branco
- Total de ativos e patrimônio exibidos no topo
- Mensagens de sucesso/erro animadas

---

##  Estrutura do Projeto

```
CRUD - CARTEIRA DE INVESTIMENTOS/
│
├── app.py                 # Aplicação Flask (backend)
├── templates/
│   └── index.html         # Interface principal (frontend)
├── static/
│   └── (opcional para CSS/JS futuros)
└── README.md              # Este arquivo
```

---

##  Configuração e Execução

### 1️ Instale as dependências:
```bash
pip install flask flask-cors oracledb
```

### 2️ Configure a conexão com o Oracle:
No arquivo `app.py`, edite a função `conectar_bd()`:
```python
connection = oracledb.connect(
    user="SEU_USUARIO",
    password="SUA_SENHA",
    dsn="localhost:1521/xe"
)
```

### 3️ Estrutura esperada no banco:

```sql
CREATE TABLE Corretoras (
  corretora_id NUMBER PRIMARY KEY,
  corretora_nome VARCHAR2(100),
  corretora_taxa_corretagem NUMBER
);

CREATE TABLE Investimentos (
  investimento_id NUMBER PRIMARY KEY,
  corretora_id NUMBER REFERENCES Corretoras(corretora_id),
  investimento_codigo VARCHAR2(20),
  investimento_tipo VARCHAR2(50),
  investimento_quantidade NUMBER,
  investimento_preco_medio NUMBER,
  investimento_data_compra DATE
);

CREATE SEQUENCE seq_investimento START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE FUNCTION fn_patrimonio_total RETURN NUMBER IS
  total NUMBER;
BEGIN
  SELECT SUM(investimento_quantidade * investimento_preco_medio)
  INTO total FROM Investimentos;
  RETURN NVL(total, 0);
END;
/

CREATE OR REPLACE PROCEDURE sp_valorizar_ativos IS
BEGIN
  UPDATE Investimentos
  SET investimento_preco_medio = investimento_preco_medio * 1.05;
  COMMIT;
END;
/
```

### 4️ Execute o servidor:
```bash
python app.py
```

Acesse no navegador:
```
http://127.0.0.1:5000
```

---


## 👨‍💻 Autor

**Thiago Sousa Leite**  
 Projeto desenvolvido para fins de * aprendizado em Python  + Banco de Dados(SQL)**  
 Contato: *tsousal177@gmail.com*  

 Se este projeto te ajudou, não esqueça de deixar uma **estrela no GitHub!**
