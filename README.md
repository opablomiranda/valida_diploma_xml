# Valida_Diploma_xml

Este é o repositório do Validador de Diploma do MEC, desenvolvido usando o Python 3.12.1 + Fast API + Selenium + Google Chrome e armazenado em container Docker.

## Visão Geral


A Rota valida um diploma no MEC.

Descrição da Solução:
O MEC não tem uma API para validar diploma de alunos, então, essa é uma automação para contornar esse problema.
Uma API que Recebe um arquivo de diploma no formato XML, envia-o para o site do MEC para validação e retorna o resultado da validação por meio de uma automação utilizando a biblitoeca Selenium. Basicamente, após receber o XML, o selenium abre o navegador Google Chrome, envia o arquivo, aguarda a validação do MEC e retorna o resultado. Esse resultado é enviado para o Endpoint, como retorno para quem está utilizando a API.

Site onde o XML é validado:

https://validadordiplomadigital.mec.gov.br/diploma


Args: file.xml (UploadFile): O arquivo de diploma no formato XML. Returns: DiplomaValidationResult: O resultado da validação do diploma.

Retornos:

"valido" : true - Indica um diploma XML validado no MEC que está em Conformidade.

"valido" : false - indica um diploma XML validado no MEC que está Inválido.


## Pré-requisitos

Primeiro, atualize os pacotes da sua distribuição, no exemplo será no ubuntu 22.04

```bash
sudo apt-get update 
```

Instale pacotes para usar um repositório HTTPS

```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

Instale o Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Após isso, clone o projeto para um diretório

```bash
git clone https://github.com/opablomiranda/valida_diploma_xml.git
```

Iremos construir o container que contém todas as dependências para a aplicação funcionar; Acesse o diretório e digite:
```bash
docker build -t valida_diploma_xml .
```

Aguarde a construção do container, assim que finalizar, vamos executá-lo

```bash
docker run -d -p 8000:8000 valida_diploma_xml ou ID do container
```
Pronto, o container subiu, para visualizar a interface do Swagger no navegador acesse:

## Acessando via OpenAPI:

http://127.0.0.1:8000/docs


## Exemplo de Requisição

curl -X 'POST'

'http://127.0.0.1:8000/diploma_upload/'

-H 'accept: application/json'

-H 'Content-Type: multipart/form-data'

-F 'file=@diploma.xml;type=text/xml'