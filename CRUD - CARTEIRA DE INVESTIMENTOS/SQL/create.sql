
-- SISTEMA DE GESTÃO DE CARTEIRA DE INVESTIMENTOS
-- CRIAÇÃO DAS TABELAS

CREATE TABLE Corretoras (
    corretora_id NUMBER PRIMARY KEY,
    corretora_nome VARCHAR2(50) NOT NULL,
    corretora_cnpj VARCHAR2(14) NOT NULL UNIQUE,
    corretora_taxa_corretagem NUMBER(5,2) NOT NULL,
    qtde_investimentos NUMBER DEFAULT 0
);

CREATE TABLE Investimentos (
    investimento_id NUMBER PRIMARY KEY,
    corretora_id NUMBER NOT NULL,
    investimento_codigo VARCHAR2(10) NOT NULL,
    investimento_tipo VARCHAR2(20) NOT NULL,
    investimento_quantidade NUMBER NOT NULL,
    investimento_preco_medio NUMBER(10,2) NOT NULL,
    investimento_data_compra DATE NOT NULL,
    CONSTRAINT fk_investimento_corretora FOREIGN KEY (corretora_id) REFERENCES Corretoras(corretora_id)
);

-- Sequences para auto-incremento
CREATE SEQUENCE seq_corretora START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_investimento START WITH 1 INCREMENT BY 1;


--  TRIGGERS
-- Trigger para incrementar qtde_investimentos ao inserir
CREATE OR REPLACE TRIGGER trg_insert_investimento
AFTER INSERT ON Investimentos
FOR EACH ROW
BEGIN
    UPDATE Corretoras 
    SET qtde_investimentos = qtde_investimentos + 1
    WHERE corretora_id = :NEW.corretora_id;
END;
/

-- Trigger para decrementar qtde_investimentos ao deletar
CREATE OR REPLACE TRIGGER trg_delete_investimento
AFTER DELETE ON Investimentos
FOR EACH ROW
BEGIN
    UPDATE Corretoras 
    SET qtde_investimentos = qtde_investimentos - 1
    WHERE corretora_id = :OLD.corretora_id;
END;
/

-- Trigger para atualizar qtde_investimentos ao mudar de corretora
CREATE OR REPLACE TRIGGER trg_update_investimento
AFTER UPDATE OF corretora_id ON Investimentos
FOR EACH ROW
BEGIN
    UPDATE Corretoras 
    SET qtde_investimentos = qtde_investimentos - 1
    WHERE corretora_id = :OLD.corretora_id;
    
    UPDATE Corretoras 
    SET qtde_investimentos = qtde_investimentos + 1
    WHERE corretora_id = :NEW.corretora_id;
END;
/


-- FUNCTION

CREATE OR REPLACE FUNCTION fn_patrimonio_total
RETURN NUMBER
IS
    v_total NUMBER;
BEGIN
    SELECT SUM(investimento_quantidade * investimento_preco_medio) 
    INTO v_total 
    FROM Investimentos;
    RETURN NVL(v_total, 0);
END;
/


-- 4. STORED PROCEDURE

CREATE OR REPLACE PROCEDURE sp_valorizar_ativos
IS
BEGIN
    UPDATE Investimentos
    SET investimento_preco_medio = investimento_preco_medio * 1.05;
    COMMIT;
END;
/


COMMIT;