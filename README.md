# Whatsapp-API

Este projeto é uma API simples construída com Flask, que utiliza Selenium para automação de tarefas em uma página web. Ele inclui autenticação usando JWT (JSON Web Tokens) e uma fila para gerenciar requisições que envolvem o uso do Selenium.

## Índice

- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Testes](#testes)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Service](#service)
- [Health-check](#health-check)

## Características

- Autenticação de usuários usando JWT.
- Enfileiramento de requisições para processamento com Selenium.
- Integração com o WebDriver para automação de navegadores.
- Validação de dados de entrada.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Selenium**: Ferramenta para automação de navegadores.
- **JWT**: Padrão para autenticação e troca de informações.
- **pytest**: Framework de testes para Python.

## Estrutura do Projeto

```
├── app
│   ├── __init__.py
│   ├── routes_health_check.py
│   ├── routes_whatsapp.py
│   └── services
│       ├── whatsapp_factory.py
│       ├── whatsapp_queue.py
│       └── whatsapp_service.py
├── app.py
├── config
│   ├── environment.py
│   ├── __init__.py
│   └── security.py
├── devtools
│   ├── dotenv.dev
│   └── dotenv.test
├── Makefile
├── pytest.ini
├── README.md
├── requirements
│   ├── base.txt
│   └── develop.txt
└── tests
    ├── test_routes_whatsapp.py
    ├── test_whatsapp_factory.py
    ├── test_whatsapp_queue.py
    └── test_whatsapp_service.py
```

## Pré-requisitos

Certifique-se de ter o Python 3.x instalado. Você também precisará das seguintes bibliotecas:

- Flask
- Flask-JWT-Extended
- Selenium
- webdriver-manager
- pytest

Você pode instalar as dependências executando:

```bash
pip install -r requirements/base.txt
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/ericmend/whatsapp-api.git
cd whatsapp-api
```

Instale as dependências:

```bash
make build-venv
source .venv/bin/activate

#desenvolvedor
make install

#producao
make requirements-prod
```

Certifique-se de que o webdriver-manager esteja configurado corretamente.

```bash
sudo apt-get install chromium-chromedriver
```

ou https://sites.google.com/chromium.org/driver/downloads

O caminho do webdriver-manager, deve ser informado na variável de ambiente `PATH_SERVICE`. Ex.:

```bash
PATH_SERVICE=/snap/bin/chromium.chromedriver
```


## Uso

Para iniciar a aplicação, execute o seguinte comando:

```bash
python app.py
```

A aplicação será iniciada em http://127.0.0.1:5000/.

## Autenticação

Para fazer requisições para as rotas protegidas, você precisará de um token JWT. Você pode implementar uma rota para autenticação de usuários e geração de tokens.
Exemplo de Requisição

Aqui está um exemplo de como fazer uma requisição para a rota /whatsapp:

```bash
curl -X POST http://127.0.0.1:5000/whatsapp \
-H "Authorization: Bearer SEU_TOKEN_JWT" \
-H "Content-Type: application/json" \
-d '{"phone_number": "+1234567890", "message": "Olá, mundo!"}'
```

## Testes

Para executar os testes unitários, use o seguinte comando:

```bash
make test
```
Os testes estão localizados na pasta tests.

## Variáveis de ambiente

| Variável            | Descrição                            |  Obrigatório |  Valor padrão |
| ------------------- | ------------------------------------ | :----------: | :-----------: |
| APP_ENV             | Ambiende do app                      | Não          | development   |
| APP_PORT            | Porta da aplicação                   | Não          | 5000          |
| PATH_SERVICE        | Local do webdriver-manager           | Sim          |               |
| PATH_CONFIG_CHROME  | Local de config do Chrome            | Sim          |               |
| PROFILE_DIRECTORY   | Nome do profile para o Chrome        | Sim          |               |
| MAX_RETRY           | Maximo de validação na inicialização | Não          | 1000          |
| SECRET_KEY          | Secret para o JWT                    | Sim          |               |
| JWT_ALGORITHM       | Tipo do algoritmo JWT                | Não          | HS256         |

## Service

Para configurar a aplicação como serviço no sistema operacional:

create file:
```bash
sudo nano /etc/systemd/system/whatsapp_api.service
```
Configura o service para iniciar a aplicação em tela (modo windows) e definir como _"active (running)"_ quando a aplicação retornar sucesso no _health-check_
```bash
[Unit]
Description=Whatsapp-API Service
After=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
TimeoutStartSec=400
ExecStart=/[PATH-CLONE-REPOSITORY]/whatsapp_api/iniciar_app.sh
ExecStartPost=/bin/bash -c 'until [ "$(curl --silent --output /dev/null --write-out "%{http_code}" http://localhost:5000/health_check)" -eq 200 ]; do echo "Aguardando o serviço responder com HTTP 200>

[Install]
WantedBy=graphical.target
```

Salva, habilita e reinicia:
```bash
sudo systemctl enable whatsapp_api.service
sudo systemctl daemon-reload
sudo systemctl restart whatsapp_api.service
```
## Health-check

Configurar um serviço para ficar validando se a aplicação está _"active (running)"_.
create file:
```bash
sudo nano /etc/systemd/system/health_check_app.service
```
```bash
[Unit]
Description=Monitorar e reiniciar o serviço caso o health_check falhe
After=network.target

[Service]
Type=simple
ExecStart=/home/eric/source/whatsapp_api/health_check_app.sh
Restart=always

[Install]
WantedBy=multi-user.target

```
Salva, habilita e reinicia:
```bash
sudo systemctl enable health_check_app.service
sudo systemctl daemon-reload
sudo systemctl restart health_check_app.service
```