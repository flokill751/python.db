import sqlite3
import os

# Caminho absoluto até o banco
base = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DB = os.path.join(base, 'dados', 'financas.db')

class BancoDeDados:
    def __init__(self, nome_arquivo=CAMINHO_DB):
        self.conexao = sqlite3.connect(nome_arquivo)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY(categoria_id) REFERENCES categoria(id)
            )
        ''')

        self.conexao.commit()

    def inserir_categoria(self, nome):
        self.cursor.execute('INSERT INTO categoria (nome) VALUES (?)', (nome,))
        self.conexao.commit()

    def listar_categorias(self):
        self.cursor.execute('SELECT * FROM categoria')
        return self.cursor.fetchall()

    def atualizar_categoria(self, id, novo_nome):
        self.cursor.execute('UPDATE categoria SET nome = ? WHERE id = ?', (novo_nome, id))
        self.conexao.commit()

    def excluir_categoria(self, id):
        self.cursor.execute('DELETE FROM categoria WHERE id = ?', (id,))
        self.conexao.commit()

    def inserir_movimentacao(self, tipo, descricao, valor, data, categoria_id):
        self.cursor.execute('''
            INSERT INTO movimentacao (tipo, descricao, valor, data, categoria_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, descricao, valor, data, categoria_id))
        self.conexao.commit()

    def listar_movimentacoes(self):
        self.cursor.execute('''
            SELECT m.id, m.tipo, m.descricao, m.valor, m.data, c.nome AS categoria
            FROM movimentacao m
            JOIN categoria c ON m.categoria_id = c.id
        ''')
        return self.cursor.fetchall()

    def atualizar_movimentacao(self, id, tipo, descricao, valor, data, categoria_id):
        self.cursor.execute('''
            UPDATE movimentacao
            SET tipo = ?, descricao = ?, valor = ?, data = ?, categoria_id = ?
            WHERE id = ?
        ''', (tipo, descricao, valor, data, categoria_id, id))
        self.conexao.commit()

    def excluir_movimentacao(self, id):
        self.cursor.execute('DELETE FROM movimentacao WHERE id = ?', (id,))
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()
