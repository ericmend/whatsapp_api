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
make install
```
Certifique-se de que o ChromeDriver esteja configurado corretamente. O webdriver-manager deve gerenciá-lo automaticamente.

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
