# Usa imagem oficial do Python
FROM python:3.11-slim

# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos do projeto para dentro da imagem
COPY . /app

# (Importante) Cria a pasta de dados
RUN mkdir -p /app/dados

# Instala dependências (se tiver um requirements.txt)
# RUN pip install -r requirements.txt

# Define o comando padrão (pode ser main.py ou outro)
CMD ["python", "main.py"]
