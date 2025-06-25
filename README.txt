
SISTEMA DE FINANÇAS PESSOAIS
============================

DESENVOLVEDORES: Felipe 
                 Ronald
DESCRIÇÃO: Sistema completo para gerenciamento de finanças pessoais com interface gráfica PyQt, banco de dados SQLite e API REST.

FUNCIONALIDADES:
- Gerenciamento de categorias (receitas e despesas)
- Registro e controle de transações financeiras
- Interface gráfica intuitiva
- API REST para integração
- Relatórios e visualizações
- Banco de dados local SQLite

TECNOLOGIAS UTILIZADAS:
- Python 3.8+
- PyQt5 (Interface Gráfica)
- SQLite (Banco de Dados)
- FastAPI (API REST)
- Pydantic (Validação de Dados)

INSTRUÇÕES DE INSTALAÇÃO:
1. Certifique-se de ter Python 3.8+ instalado
2. Navegue até a pasta do projeto
3. Crie um ambiente virtual: python -m venv venv
4. Ative o ambiente virtual:
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate
5. Instale as dependências: pip install -r requirements.txt

INSTRUÇÕES DE EXECUÇÃO:
1. Para executar apenas a interface gráfica:
   python main.py

2. Para executar apenas a API:
   uvicorn api:app --host 0.0.0.0 --port 8001
   Acesse: http://localhost:8001/docs (Documentação Swagger)

3. Para executar ambos simultaneamente:
   python main.py (a API pode ser iniciada automaticamente)

ESTRUTURA DO BANCO DE DADOS:
- Tabela 'categorias': id, nome, tipo
- Tabela 'transacoes': id, descricao, valor, data, categoria_id
- Relacionamento: transacoes.categoria_id -> categorias.id

COMO USAR:
1. Inicie o sistema com python main.py
2. Use a aba "Categorias" para criar categorias de receita e despesa
3. Use a aba "Transações" para registrar movimentações financeiras
4. Visualize relatórios na aba "Relatórios"
5. A API estará disponível em http://localhost:8000

ENDPOINTS DA API:
- GET /categorias - Listar categorias
- POST /categorias - Criar categoria
- PUT /categorias/{id} - Atualizar categoria
- DELETE /categorias/{id} - Excluir categoria
- GET /transacoes - Listar transações
- POST /transacoes - Criar transação
- PUT /transacoes/{id} - Atualizar transação
- DELETE /transacoes/{id} - Excluir transação

OBSERVAÇÕES:
- O banco de dados será criado automaticamente na primeira execução
- Dados de exemplo são inseridos automaticamente
- Todas as operações incluem validação de dados
- Interface responsiva e amigável ao usuário
