# Use a imagem oficial do Python 3.9 como base
FROM python:3.12.1

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho dentro do contêiner
COPY . /src

WORKDIR /src

# Instala as dependências do projeto usando o Poetry
RUN poetry install --no-root --no-dev

# Instala o Chrome Driver
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Expõe a porta em que sua aplicação será executada
EXPOSE 8000

# Comando para iniciar sua aplicação quando o contêiner for iniciado
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host","0.0.0.0","--port", "8000"]
