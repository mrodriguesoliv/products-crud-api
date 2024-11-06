FROM python:3.11

WORKDIR /app

# Copiar requirements.txt e instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -v

# Copiar todo o conteúdo da aplicação para o container
COPY . .

# Expor a porta
EXPOSE 8000

# Definir o comando padrão para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
