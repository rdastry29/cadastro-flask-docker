# Usar imagem base do Python
FROM python:3.9

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos para o container
COPY . .

# Instalar dependências
RUN pip install flask

# Expor porta 5000
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
