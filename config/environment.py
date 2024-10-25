import os
from dotenv import load_dotenv

class Environment:
    def __init__(self):
        # Carrega variáveis do arquivo .env
        load_dotenv()
        
        # Recupera valores das variáveis de ambiente
        self.APP_PORT = self.get_app_port()
        self.PATH_SERVICE = os.getenv("PATH_SERVICE", "/caminho/padrão/para/chromedriver")
        self.PATH_CONFIG_CHROME = os.getenv("PATH_CONFIG_CHROME", "/caminho/padrão/para/google-chrome")
        self.PROFILE_DIRECTORY = os.getenv("PROFILE_DIRECTORY", "PastaPadrão")
        self.MAX_RETRY = self.get_max_retry()
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
        self.JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
        self.PAGE_LOAD_TIMEOUT = self.get_page_load_timeout()

    def get_max_retry(self):
        max_retry = os.getenv("MAX_RETRY", "1000")
        try:
            max_retry = int(max_retry)
        except ValueError:
            raise ValueError("A variável de ambiente 'MAX_RETRY' deve ser um número inteiro.")
        if max_retry <= 0:
            raise EnvironmentError("A variável de ambiente 'MAX_RETRY' deve ser maior que zero.")
        return max_retry

    def get_app_port(self):
        app_port = os.getenv("APP_PORT", "5000")
        try:
            app_port = int(app_port)
        except ValueError:
            raise ValueError("A variável de ambiente 'APP_PORT' deve ser um número inteiro.")
        if app_port <= 0:
            raise EnvironmentError("A variável de ambiente 'APP_PORT' deve ser maior que zero.")
        return app_port

    def get_page_load_timeout(self):
        page_load_timeout = os.getenv("PAGE_LOAD_TIMEOUT", "600")
        try:
            page_load_timeout = int(page_load_timeout)
        except ValueError:
            raise ValueError("A variável de ambiente 'PAGE_LOAD_TIMEOUT' deve ser um número inteiro.")
        if page_load_timeout <= 0:
            raise EnvironmentError("A variável de ambiente 'PAGE_LOAD_TIMEOUT' deve ser maior que zero.")
        return page_load_timeout
