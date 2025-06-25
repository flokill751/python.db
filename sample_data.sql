
-- Dados de exemplo para o sistema de finanças pessoais

-- Categorias de exemplo
INSERT INTO categorias (nome, tipo) VALUES 
('Salário', 'receita'),
('Freelance', 'receita'),
('Investimentos', 'receita'),
('Alimentação', 'despesa'),
('Transporte', 'despesa'),
('Moradia', 'despesa'),
('Lazer', 'despesa'),
('Saúde', 'despesa'),
('Educação', 'despesa');

-- Transações de exemplo
INSERT INTO transacoes (descricao, valor, data, categoria_id) VALUES 
('Salário Janeiro', 5000.00, '2024-01-01', 1),
('Projeto Web', 1500.00, '2024-01-15', 2),
('Dividendos', 200.00, '2024-01-20', 3),
('Supermercado', -350.00, '2024-01-02', 4),
('Combustível', -200.00, '2024-01-03', 5),
('Aluguel', -1200.00, '2024-01-01', 6),
('Cinema', -50.00, '2024-01-10', 7),
('Consulta médica', -150.00, '2024-01-12', 8),
('Curso online', -99.00, '2024-01-18', 9),
('Restaurante', -80.00, '2024-01-25', 4);
