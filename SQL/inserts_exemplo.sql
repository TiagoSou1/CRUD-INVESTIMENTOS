--  DADOS DE EXEMPLO
-- Inserindo corretoras
INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Corretora Alpha', '00000000000001', 10.00);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Corretora Beta', '00000000000002', 8.50);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Corretora Gamma', '00000000000003', 12.00);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Corretora Delta', '00000000000004', 7.00);

-- Inserindo investimentos
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 1, 'PETR4', 'Acao', 100, 28.50, TO_DATE('2024-01-15', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 1, 'VALE3', 'Acao', 50, 65.80, TO_DATE('2024-02-20', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 2, 'ITUB4', 'Acao', 200, 32.40, TO_DATE('2024-03-10', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 2, 'BBAS3', 'Acao', 80, 48.90, TO_DATE('2024-01-25', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 3, 'MXRF11', 'FII', 150, 10.20, TO_DATE('2024-02-05', 'YYYY-MM-DD'));

COMMIT;
