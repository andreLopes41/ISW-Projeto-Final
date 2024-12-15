# Use a imagem oficial do Python como base
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e o código da aplicação para o contêiner
COPY requirements.txt .
COPY . .

# Instale as dependências Python
RUN pip install oci 
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para executar a aplicação fastAPI
CMD ["uvicorn", "view.main:app", "--host", "0.0.0.0", "--port", "8000"]
