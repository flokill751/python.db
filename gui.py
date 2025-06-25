
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QDateEdit, QMessageBox, QFormLayout,
                             QGroupBox, QGridLayout, QHeaderView, QDoubleSpinBox,
                             QTextEdit, QSplitter, QFrame)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from datetime import datetime, date
from db import DatabaseManager
from models import Categoria, Transacao

class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.selected_categoria_id = None
        self.selected_transacao_id = None
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Sistema de Finanças Pessoais")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Sistema de Finanças Pessoais")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Resumo financeiro
        self.create_resumo_widget(main_layout)
        
        # Abas principais
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Criar abas
        self.create_categorias_tab()
        self.create_transacoes_tab()
        self.create_relatorios_tab()
        
        # Aplicar estilo
        self.apply_styles()
    
    def apply_styles(self):
        """Aplica estilos à interface"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: black;
            }
            QTabBar::tab {
                background-color: #bdc3c7;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
            }
        """)
    
    def create_resumo_widget(self, parent_layout):
        """Cria o widget de resumo financeiro"""
        resumo_frame = QFrame()
        resumo_frame.setFrameStyle(QFrame.Box)
        resumo_frame.setStyleSheet("background-color: white; border: 1px solid #bdc3c7; border-radius: 8px; margin: 5px;")
        
        resumo_layout = QHBoxLayout()
        resumo_frame.setLayout(resumo_layout)
        
        # Labels para exibir informações
        self.saldo_label = QLabel("Lucro: R$ 0,00")
        self.receitas_label = QLabel("Receitas: R$ 0,00")
        self.despesas_label = QLabel("Despesas: R$ 0,00")
        
        # Estilo para os labels
        label_style = "font-size: 14px; font-weight: bold; padding: 10px; margin: 5px;"
        self.saldo_label.setStyleSheet(label_style + "color: #27ae60;")
        self.receitas_label.setStyleSheet(label_style + "color: #2ecc71;")
        self.despesas_label.setStyleSheet(label_style + "color: #e74c3c;")
        
        resumo_layout.addWidget(self.saldo_label)
        resumo_layout.addWidget(self.receitas_label)
        resumo_layout.addWidget(self.despesas_label)
        
        parent_layout.addWidget(resumo_frame)
    
    def create_categorias_tab(self):
        """Cria a aba de categorias"""
        categorias_widget = QWidget()
        layout = QHBoxLayout()
        categorias_widget.setLayout(layout)
        
        # Formulário de categorias
        form_group = QGroupBox("Gerenciar Categorias")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        self.categoria_nome_edit = QLineEdit()
        self.categoria_tipo_combo = QComboBox()
        self.categoria_tipo_combo.addItems(["receita", "despesa"])
        
        form_layout.addRow("Nome:", self.categoria_nome_edit)
        form_layout.addRow("Tipo:", self.categoria_tipo_combo)
        
        # Botões
        buttons_layout = QHBoxLayout()
        self.add_categoria_btn = QPushButton("Adicionar")
        self.update_categoria_btn = QPushButton("Atualizar")
        self.delete_categoria_btn = QPushButton("Excluir")
        self.clear_categoria_btn = QPushButton("Limpar")
        
        self.add_categoria_btn.clicked.connect(self.add_categoria)
        self.update_categoria_btn.clicked.connect(self.update_categoria)
        self.delete_categoria_btn.clicked.connect(self.delete_categoria)
        self.clear_categoria_btn.clicked.connect(self.clear_categoria_form)
        
        buttons_layout.addWidget(self.add_categoria_btn)
        buttons_layout.addWidget(self.update_categoria_btn)
        buttons_layout.addWidget(self.delete_categoria_btn)
        buttons_layout.addWidget(self.clear_categoria_btn)
        
        form_layout.addRow(buttons_layout)
        
        # Tabela de categorias
        self.categorias_table = QTableWidget()
        self.categorias_table.setColumnCount(3)
        self.categorias_table.setHorizontalHeaderLabels(["ID", "Nome", "Tipo"])
        self.categorias_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.categorias_table.itemSelectionChanged.connect(self.on_categoria_selected)
        
        layout.addWidget(form_group)
        layout.addWidget(self.categorias_table)
        
        self.tab_widget.addTab(categorias_widget, "Categorias")
    
    def create_transacoes_tab(self):
        """Cria a aba de transações"""
        transacoes_widget = QWidget()
        layout = QHBoxLayout()
        transacoes_widget.setLayout(layout)
        
        # Formulário de transações
        form_group = QGroupBox("Gerenciar Transações")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        self.transacao_descricao_edit = QLineEdit()
        self.transacao_valor_spin = QDoubleSpinBox()
        self.transacao_valor_spin.setRange(-999999.99, 999999.99)
        self.transacao_valor_spin.setDecimals(2)
        self.transacao_data_edit = QDateEdit()
        self.transacao_data_edit.setDate(QDate.currentDate())
        self.transacao_categoria_combo = QComboBox()
        
        form_layout.addRow("Descrição:", self.transacao_descricao_edit)
        form_layout.addRow("Valor:", self.transacao_valor_spin)
        form_layout.addRow("Data:", self.transacao_data_edit)
        form_layout.addRow("Categoria:", self.transacao_categoria_combo)
        
        # Botões
        buttons_layout = QHBoxLayout()
        self.add_transacao_btn = QPushButton("Adicionar")
        self.update_transacao_btn = QPushButton("Atualizar")
        self.delete_transacao_btn = QPushButton("Excluir")
        self.clear_transacao_btn = QPushButton("Limpar")
        
        self.add_transacao_btn.clicked.connect(self.add_transacao)
        self.update_transacao_btn.clicked.connect(self.update_transacao)
        self.delete_transacao_btn.clicked.connect(self.delete_transacao)
        self.clear_transacao_btn.clicked.connect(self.clear_transacao_form)
        
        buttons_layout.addWidget(self.add_transacao_btn)
        buttons_layout.addWidget(self.update_transacao_btn)
        buttons_layout.addWidget(self.delete_transacao_btn)
        buttons_layout.addWidget(self.clear_transacao_btn)
        
        form_layout.addRow(buttons_layout)
        
        # Tabela de transações
        self.transacoes_table = QTableWidget()
        self.transacoes_table.setColumnCount(5)
        self.transacoes_table.setHorizontalHeaderLabels(["ID", "Descrição", "Valor", "Data", "Categoria"])
        self.transacoes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transacoes_table.itemSelectionChanged.connect(self.on_transacao_selected)
        
        layout.addWidget(form_group)
        layout.addWidget(self.transacoes_table)
        
        self.tab_widget.addTab(transacoes_widget, "Transações")
    
    def create_relatorios_tab(self):
        """Cria a aba de relatórios"""
        relatorios_widget = QWidget()
        layout = QVBoxLayout()
        relatorios_widget.setLayout(layout)
        
        # Botão para atualizar relatórios
        refresh_btn = QPushButton("Atualizar Relatórios")
        refresh_btn.clicked.connect(self.update_relatorios)
        layout.addWidget(refresh_btn)
        
        # Área de texto para relatórios
        self.relatorios_text = QTextEdit()
        self.relatorios_text.setReadOnly(True)
        layout.addWidget(self.relatorios_text)
        
        self.tab_widget.addTab(relatorios_widget, "Relatórios")
    
    def load_data(self):
        """Carrega dados do banco de dados"""
        self.load_categorias()
        self.load_transacoes()
        self.update_resumo()
        self.update_categoria_combo()
    
    def load_categorias(self):
        """Carrega categorias na tabela"""
        categorias = self.db.get_categorias()
        self.categorias_table.setRowCount(len(categorias))
        
        for row, categoria in enumerate(categorias):
            self.categorias_table.setItem(row, 0, QTableWidgetItem(str(categoria.id)))
            self.categorias_table.setItem(row, 1, QTableWidgetItem(categoria.nome))
            self.categorias_table.setItem(row, 2, QTableWidgetItem(categoria.tipo))
    
    def load_transacoes(self):
        """Carrega transações na tabela"""
        transacoes = self.db.get_transacoes()
        self.transacoes_table.setRowCount(len(transacoes))
        
        for row, transacao in enumerate(transacoes):
            self.transacoes_table.setItem(row, 0, QTableWidgetItem(str(transacao.id)))
            self.transacoes_table.setItem(row, 1, QTableWidgetItem(transacao.descricao))
            self.transacoes_table.setItem(row, 2, QTableWidgetItem(f"R$ {transacao.valor:.2f}"))
            data_str = transacao.data.strftime('%d/%m/%Y') if isinstance(transacao.data, datetime) else str(transacao.data)
            self.transacoes_table.setItem(row, 3, QTableWidgetItem(data_str))
            self.transacoes_table.setItem(row, 4, QTableWidgetItem(transacao.categoria_nome or ""))
    
    def update_categoria_combo(self):
        """Atualiza o combo de categorias"""
        self.transacao_categoria_combo.clear()
        categorias = self.db.get_categorias()
        for categoria in categorias:
            self.transacao_categoria_combo.addItem(f"{categoria.nome} ({categoria.tipo})", categoria.id)
    
    def update_resumo(self):
        """Atualiza o resumo financeiro"""
        saldo = self.db.get_saldo_total()
        receitas = self.db.get_total_receitas()
        despesas = self.db.get_total_despesas()
        
        self.saldo_label.setText(f"Saldo: R$ {saldo:.2f}")
        self.receitas_label.setText(f"Receitas: R$ {receitas:.2f}")
        self.despesas_label.setText(f"Despesas: R$ {despesas:.2f}")
    
    def add_categoria(self):
        """Adiciona uma nova categoria"""
        nome = self.categoria_nome_edit.text().strip()
        tipo = self.categoria_tipo_combo.currentText()
        
        if not nome:
            QMessageBox.warning(self, "Erro", "Nome da categoria é obrigatório!")
            return
        
        try:
            self.db.create_categoria(nome, tipo)
            QMessageBox.information(self, "Sucesso", "Categoria adicionada com sucesso!")
            self.clear_categoria_form()
            self.load_categorias()
            self.update_categoria_combo()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
    
    def update_categoria(self):
        """Atualiza uma categoria existente"""
        if not self.selected_categoria_id:
            QMessageBox.warning(self, "Erro", "Selecione uma categoria para atualizar!")
            return
        
        nome = self.categoria_nome_edit.text().strip()
        tipo = self.categoria_tipo_combo.currentText()
        
        if not nome:
            QMessageBox.warning(self, "Erro", "Nome da categoria é obrigatório!")
            return
        
        try:
            self.db.update_categoria(self.selected_categoria_id, nome, tipo)
            QMessageBox.information(self, "Sucesso", "Categoria atualizada com sucesso!")
            self.clear_categoria_form()
            self.load_categorias()
            self.update_categoria_combo()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
    
    def delete_categoria(self):
        """Exclui uma categoria"""
        if not self.selected_categoria_id:
            QMessageBox.warning(self, "Erro", "Selecione uma categoria para excluir!")
            return
        
        reply = QMessageBox.question(self, "Confirmar", "Tem certeza que deseja excluir esta categoria?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_categoria(self.selected_categoria_id)
                QMessageBox.information(self, "Sucesso", "Categoria excluída com sucesso!")
                self.clear_categoria_form()
                self.load_categorias()
                self.update_categoria_combo()
            except ValueError as e:
                QMessageBox.warning(self, "Erro", str(e))
    
    def clear_categoria_form(self):
        """Limpa o formulário de categoria"""
        self.categoria_nome_edit.clear()
        self.categoria_tipo_combo.setCurrentIndex(0)
        self.selected_categoria_id = None
    
    def on_categoria_selected(self):
        """Evento quando uma categoria é selecionada"""
        current_row = self.categorias_table.currentRow()
        if current_row >= 0:
            id_item = self.categorias_table.item(current_row, 0)
            nome_item = self.categorias_table.item(current_row, 1)
            tipo_item = self.categorias_table.item(current_row, 2)
            
            if id_item and nome_item and tipo_item:
                self.selected_categoria_id = int(id_item.text())
                self.categoria_nome_edit.setText(nome_item.text())
                self.categoria_tipo_combo.setCurrentText(tipo_item.text())
    
    def add_transacao(self):
        """Adiciona uma nova transação"""
        descricao = self.transacao_descricao_edit.text().strip()
        valor = self.transacao_valor_spin.value()
        data = self.transacao_data_edit.date().toPyDate()
        categoria_id = self.transacao_categoria_combo.currentData()
        
        if not descricao:
            QMessageBox.warning(self, "Erro", "Descrição da transação é obrigatória!")
            return
        
        if not categoria_id:
            QMessageBox.warning(self, "Erro", "Selecione uma categoria!")
            return
        
        try:
            data_str = data.strftime('%Y-%m-%d')
            self.db.create_transacao(descricao, valor, data_str, categoria_id)
            QMessageBox.information(self, "Sucesso", "Transação adicionada com sucesso!")
            self.clear_transacao_form()
            self.load_transacoes()
            self.update_resumo()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
    
    def update_transacao(self):
        """Atualiza uma transação existente"""
        if not self.selected_transacao_id:
            QMessageBox.warning(self, "Erro", "Selecione uma transação para atualizar!")
            return
        
        descricao = self.transacao_descricao_edit.text().strip()
        valor = self.transacao_valor_spin.value()
        data = self.transacao_data_edit.date().toPyDate()
        categoria_id = self.transacao_categoria_combo.currentData()
        
        if not descricao:
            QMessageBox.warning(self, "Erro", "Descrição da transação é obrigatória!")
            return
        
        if not categoria_id:
            QMessageBox.warning(self, "Erro", "Selecione uma categoria!")
            return
        
        try:
            data_str = data.strftime('%Y-%m-%d')
            self.db.update_transacao(self.selected_transacao_id, descricao, valor, data_str, categoria_id)
            QMessageBox.information(self, "Sucesso", "Transação atualizada com sucesso!")
            self.clear_transacao_form()
            self.load_transacoes()
            self.update_resumo()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
    
    def delete_transacao(self):
        """Exclui uma transação"""
        if not self.selected_transacao_id:
            QMessageBox.warning(self, "Erro", "Selecione uma transação para excluir!")
            return
        
        reply = QMessageBox.question(self, "Confirmar", "Tem certeza que deseja excluir esta transação?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_transacao(self.selected_transacao_id)
                QMessageBox.information(self, "Sucesso", "Transação excluída com sucesso!")
                self.clear_transacao_form()
                self.load_transacoes()
                self.update_resumo()
            except Exception as e:
                QMessageBox.warning(self, "Erro", str(e))
    
    def clear_transacao_form(self):
        """Limpa o formulário de transação"""
        self.transacao_descricao_edit.clear()
        self.transacao_valor_spin.setValue(0.0)
        self.transacao_data_edit.setDate(QDate.currentDate())
        self.transacao_categoria_combo.setCurrentIndex(0)
        self.selected_transacao_id = None
    
    def on_transacao_selected(self):
        """Evento quando uma transação é selecionada"""
        current_row = self.transacoes_table.currentRow()
        if current_row >= 0:
            id_item = self.transacoes_table.item(current_row, 0)
            descricao_item = self.transacoes_table.item(current_row, 1)
            valor_item = self.transacoes_table.item(current_row, 2)
            data_item = self.transacoes_table.item(current_row, 3)
            
            if id_item and descricao_item and valor_item and data_item:
                self.selected_transacao_id = int(id_item.text())
                self.transacao_descricao_edit.setText(descricao_item.text())
                
                # Extrair valor numérico
                valor_text = valor_item.text().replace("R$ ", "").replace(",", ".")
                try:
                    valor = float(valor_text)
                    self.transacao_valor_spin.setValue(valor)
                except ValueError:
                    self.transacao_valor_spin.setValue(0.0)
                
                # Converter data
                try:
                    data_parts = data_item.text().split('/')
                    if len(data_parts) == 3:
                        day, month, year = data_parts
                        qdate = QDate(int(year), int(month), int(day))
                        self.transacao_data_edit.setDate(qdate)
                except:
                    self.transacao_data_edit.setDate(QDate.currentDate())
                
                # Buscar categoria da transação
                transacao = self.db.get_transacao_by_id(self.selected_transacao_id)
                if transacao:
                    for i in range(self.transacao_categoria_combo.count()):
                        if self.transacao_categoria_combo.itemData(i) == transacao.categoria_id:
                            self.transacao_categoria_combo.setCurrentIndex(i)
                            break
    
    def update_relatorios(self):
        """Atualiza os relatórios"""
        try:
            saldo = self.db.get_saldo_total()
            receitas = self.db.get_total_receitas()
            despesas = self.db.get_total_despesas()
            categorias = self.db.get_categorias()
            transacoes = self.db.get_transacoes()
            
            relatorio = f"""
RELATÓRIO FINANCEIRO
====================

RESUMO GERAL:
• Saldo Total: R$ {saldo:.2f}
• Total de Receitas: R$ {receitas:.2f}
• Total de Despesas: R$ {despesas:.2f}
• Total de Categorias: {len(categorias)}
• Total de Transações: {len(transacoes)}

CATEGORIAS:
"""
            
            for categoria in categorias:
                transacoes_cat = self.db.get_transacoes_by_categoria(categoria.id)
                total_cat = sum(t.valor for t in transacoes_cat)
                relatorio += f"• {categoria.nome} ({categoria.tipo}): R$ {total_cat:.2f} ({len(transacoes_cat)} transações)\n"
            
            relatorio += "\n\nÚLTIMAS TRANSAÇÕES:\n"
            for i, transacao in enumerate(transacoes[:10]):  # Últimas 10 transações
                data_str = transacao.data.strftime('%d/%m/%Y') if isinstance(transacao.data, datetime) else str(transacao.data)
                relatorio += f"• {data_str} - {transacao.descricao}: R$ {transacao.valor:.2f} ({transacao.categoria_nome})\n"
            
            self.relatorios_text.setText(relatorio)
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao gerar relatório: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
