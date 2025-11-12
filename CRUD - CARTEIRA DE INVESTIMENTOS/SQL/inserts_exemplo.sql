--  DADOS DE EXEMPLO
-- Inserindo corretoras
INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'XP Investimentos', '02332886000104', 10.00);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Rico Investimentos', '03375874000134', 8.50);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'BTG Pactual', '30306294000145', 12.00);

INSERT INTO Corretoras (corretora_id, corretora_nome, corretora_cnpj, corretora_taxa_corretagem) 
VALUES (seq_corretora.NEXTVAL, 'Clear Corretora', '02558157000162', 7.00);

-- Inserindo investimentos
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 1, 'PETR4', 'Acao', 100, 28.50, TO_DATE('2024-01-15', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 1, 'VALE3', 'Acao', 50, 65.80, TO_DATE('2024-02-20', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 2, 'ITUB4', 'Acao', 200, 32.40, TO_DATE('2024-03-10', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 2, 'BBAS3', 'Acao', 80, 48.90, TO_DATE('2024-01-25', 'YYYY-MM-DD'));
INSERT INTO Investimentos VALUES (seq_investimento.NEXTVAL, 3, 'MXRF11', 'FII', 150, 10.20, TO_DATE('2024-02-05', 'YYYY-MM-DD'));

COMMIT;