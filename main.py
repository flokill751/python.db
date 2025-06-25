
import sys
import subprocess
import threading
from PyQt5.QtWidgets import QApplication
from gui import FinanceApp

def start_api():
    """Inicia a API em uma thread separada"""
    try:

        subprocess.run([sys.executable, "api.py"], check=True)
    
    except Exception as e:
        print(f"Erro ao iniciar API: {e}")

def main():
    """Função principal que inicia a aplicação"""
    # Iniciar API em background (opcional)
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Iniciar interface gráfica
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
