FROM python:3.12.1

# Instale o Poetry
RUN pip install poetry

# Define o diretório de trabalho dentro do contêiner
COPY . /src

# Aqui a gente define o diretório de trabalho
WORKDIR /src

# Instala as dependências do projeto usando o Poetry
RUN poetry install --no-root --no-dev

# Instala o Chrome Driver (Pra poder abrir a automação do Selenium)
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Abaixo a gente expõe a porta que o container vai trabalhar na máquina.
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for iniciado (Roda o Server do Uvicorn)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host","0.0.0.0","--port", "8000"]
