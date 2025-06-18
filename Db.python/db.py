import sqlite3
import os

base = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DB = os.path.join(base, 'dados', 'financas.db')

class BancoDeDados:
    def __init__(self, nome_arquivo=CAMINHO_DB):
        self.nome_arquivo = nome_arquivo
        self.criar_tabelas()

    def _get_conexao(self):
        # Cria uma nova conexão a cada uso, com check_same_thread=False para evitar erro de thread
        return sqlite3.connect(self.nome_arquivo, check_same_thread=False)

    def criar_tabelas(self):
        conn = self._get_conexao()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')

        cursor.execute('''
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

        conn.commit()
        conn.close()

    def inserir_categoria(self, nome):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categoria (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    def listar_categorias(self):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categoria')
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def atualizar_categoria(self, id, novo_nome):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE categoria SET nome = ? WHERE id = ?', (novo_nome, id))
        conn.commit()
        conn.close()

    def excluir_categoria(self, id):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categoria WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def inserir_movimentacao(self, tipo, descricao, valor, data, categoria_id):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movimentacao (tipo, descricao, valor, data, categoria_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, descricao, valor, data, categoria_id))
        conn.commit()
        conn.close()

    def listar_movimentacoes(self):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.id, m.tipo, m.descricao, m.valor, m.data, c.nome AS categoria
            FROM movimentacao m
            JOIN categoria c ON m.categoria_id = c.id
        ''')
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def atualizar_movimentacao(self, id, tipo, descricao, valor, data, categoria_id):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE movimentacao
            SET tipo = ?, descricao = ?, valor = ?, data = ?, categoria_id = ?
            WHERE id = ?
        ''', (tipo, descricao, valor, data, categoria_id, id))
        conn.commit()
        conn.close()

    def excluir_movimentacao(self, id):
        conn = self._get_conexao()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movimentacao WHERE id = ?', (id,))
        conn.commit()
        conn.close()
