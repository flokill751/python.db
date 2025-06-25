
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple
from models import Categoria, Transacao

class DatabaseManager:
    def __init__(self, db_path: str = "finance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Criar tabela categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                tipo TEXT NOT NULL CHECK (tipo IN ('receita', 'despesa'))
            )
        ''')
        
        # Criar tabela transacoes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Popular com dados de exemplo se estiver vazio
        self.populate_sample_data()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def populate_sample_data(self):
        """Popula o banco com dados de exemplo se estiver vazio"""
        if self.get_categoria_count() == 0:
            # Inserir categorias de exemplo
            categorias_exemplo = [
                ('Salário', 'receita'),
                ('Freelance', 'receita'),
                ('Investimentos', 'receita'),
                ('Alimentação', 'despesa'),
                ('Transporte', 'despesa'),
                ('Moradia', 'despesa'),
                ('Lazer', 'despesa'),
                ('Saúde', 'despesa'),
                ('Educação', 'despesa')
            ]
            
            for nome, tipo in categorias_exemplo:
                self.create_categoria(nome, tipo)
            
            # Inserir transações de exemplo
            transacoes_exemplo = [
                ('Salário Janeiro', 5000.00, '2024-01-01', 1),
                ('Projeto Web', 1500.00, '2024-01-15', 2),
                ('Dividendos', 200.00, '2024-01-20', 3),
                ('Supermercado', -350.00, '2024-01-02', 4),
                ('Combustível', -200.00, '2024-01-03', 5),
                ('Aluguel', -1200.00, '2024-01-01', 6),
                ('Cinema', -50.00, '2024-01-10', 7),
                ('Consulta médica', -150.00, '2024-01-12', 8),
                ('Curso online', -99.00, '2024-01-18', 9),
                ('Restaurante', -80.00, '2024-01-25', 4)
            ]
            
            for desc, valor, data, cat_id in transacoes_exemplo:
                self.create_transacao(desc, valor, data, cat_id)
    
    # CRUD para Categorias
    def create_categoria(self, nome: str, tipo: str) -> int:
        """Cria uma nova categoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO categorias (nome, tipo) VALUES (?, ?)', (nome, tipo))
            categoria_id = cursor.lastrowid
            conn.commit()
            return categoria_id
        except sqlite3.IntegrityError:
            raise ValueError(f"Categoria '{nome}' já existe")
        finally:
            conn.close()
    
    def get_categorias(self) -> List[Categoria]:
        """Retorna todas as categorias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, tipo FROM categorias ORDER BY tipo, nome')
        rows = cursor.fetchall()
        conn.close()
        return [Categoria(id=row[0], nome=row[1], tipo=row[2]) for row in rows]
    
    def get_categoria_by_id(self, categoria_id: int) -> Optional[Categoria]:
        """Retorna uma categoria pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, tipo FROM categorias WHERE id = ?', (categoria_id,))
        row = cursor.fetchone()
        conn.close()
        return Categoria(id=row[0], nome=row[1], tipo=row[2]) if row else None
    
    def update_categoria(self, categoria_id: int, nome: str, tipo: str) -> bool:
        """Atualiza uma categoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE categorias SET nome = ?, tipo = ? WHERE id = ?', 
                         (nome, tipo, categoria_id))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except sqlite3.IntegrityError:
            raise ValueError(f"Categoria '{nome}' já existe")
        finally:
            conn.close()
    
    def delete_categoria(self, categoria_id: int) -> bool:
        """Exclui uma categoria (se não tiver transações associadas)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar se há transações associadas
        cursor.execute('SELECT COUNT(*) FROM transacoes WHERE categoria_id = ?', (categoria_id,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            raise ValueError("Não é possível excluir categoria com transações associadas")
        
        cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_categoria_count(self) -> int:
        """Retorna o número de categorias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM categorias')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    # CRUD para Transações
    def create_transacao(self, descricao: str, valor: float, data: str, categoria_id: int) -> int:
        """Cria uma nova transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transacoes (descricao, valor, data, categoria_id) VALUES (?, ?, ?, ?)',
                      (descricao, valor, data, categoria_id))
        transacao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transacao_id
    
    def get_transacoes(self) -> List[Transacao]:
        """Retorna todas as transações com informações da categoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.descricao, t.valor, t.data, t.categoria_id, c.nome
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            ORDER BY t.data DESC, t.id DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        transacoes = []
        for row in rows:
            data_obj = datetime.strptime(row[3], '%Y-%m-%d') if isinstance(row[3], str) else row[3]
            transacoes.append(Transacao(
                id=row[0],
                descricao=row[1],
                valor=row[2],
                data=data_obj,
                categoria_id=row[4],
                categoria_nome=row[5]
            ))
        return transacoes
    
    def get_transacao_by_id(self, transacao_id: int) -> Optional[Transacao]:
        """Retorna uma transação pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.descricao, t.valor, t.data, t.categoria_id, c.nome
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.id = ?
        ''', (transacao_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            data_obj = datetime.strptime(row[3], '%Y-%m-%d') if isinstance(row[3], str) else row[3]
            return Transacao(
                id=row[0],
                descricao=row[1],
                valor=row[2],
                data=data_obj,
                categoria_id=row[4],
                categoria_nome=row[5]
            )
        return None
    
    def update_transacao(self, transacao_id: int, descricao: str, valor: float, 
                        data: str, categoria_id: int) -> bool:
        """Atualiza uma transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transacoes 
            SET descricao = ?, valor = ?, data = ?, categoria_id = ? 
            WHERE id = ?
        ''', (descricao, valor, data, categoria_id, transacao_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_transacao(self, transacao_id: int) -> bool:
        """Exclui uma transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transacoes WHERE id = ?', (transacao_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_transacoes_by_categoria(self, categoria_id: int) -> List[Transacao]:
        """Retorna transações de uma categoria específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.descricao, t.valor, t.data, t.categoria_id, c.nome
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.categoria_id = ?
            ORDER BY t.data DESC
        ''', (categoria_id,))
        rows = cursor.fetchall()
        conn.close()
        
        transacoes = []
        for row in rows:
            data_obj = datetime.strptime(row[3], '%Y-%m-%d') if isinstance(row[3], str) else row[3]
            transacoes.append(Transacao(
                id=row[0],
                descricao=row[1],
                valor=row[2],
                data=data_obj,
                categoria_id=row[4],
                categoria_nome=row[5]
            ))
        return transacoes
    
    def get_saldo_total(self) -> float:
        """Calcula o saldo total (receitas - despesas)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(valor) FROM transacoes')
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    def get_total_receitas(self) -> float:
        """Calcula o total de receitas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(t.valor) FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE c.tipo = 'receita'
        ''')
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    def get_total_despesas(self) -> float:
        """Calcula o total de despesas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(ABS(t.valor)) FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE c.tipo = 'despesa'
        ''')
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0

if __name__ == "__main__":
    # Criar banco e popular com dados de exemplo
    db = DatabaseManager()
    print("Banco de dados criado com sucesso!")
    print(f"Categorias: {len(db.get_categorias())}")
    print(f"Transações: {len(db.get_transacoes())}")
    print(f"Saldo total: R$ {db.get_saldo_total():.2f}")
