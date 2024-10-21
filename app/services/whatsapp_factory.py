import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config.environment import Environment

env = Environment()


class WebDriverWhatsappFactory:
    _driver = None  # Atributo estático para armazenar a instância do WebDriver

    @staticmethod
    def _validate_driver():
        WebDriverWait(WebDriverWhatsappFactory._driver, 6000)
        index = 0
        while index < env.MAX_RETRY:
            index += 1
            elements_recipient = (
                WebDriverWhatsappFactory._driver.find_elements(
                    By.CSS_SELECTOR, "div._ak9t"
                )
            )
            if len(elements_recipient) > 0:
                return True
            time.sleep(5)
        return False

    @staticmethod
    def create_driver(retry: int = 0):
        """Cria uma instância do WebDriver Chrome, se ainda não existir,
        e navega até a página inicial."""
        if WebDriverWhatsappFactory._driver is None:
            options = Options()
            options.add_argument(
                f"--profile-directory={env.PROFILE_DIRECTORY}"
            )
            options.add_argument(f"--user-data-dir={env.PATH_CONFIG_CHROME}")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            # options.add_argument('--headless')
            WebDriverWhatsappFactory._driver = webdriver.Chrome(
                service=Service(executable_path=env.PATH_SERVICE),
                options=options,
            )
            WebDriverWhatsappFactory._driver.get("https://web.whatsapp.com")
        if not WebDriverWhatsappFactory._validate_driver():
            if retry <= 3:
                retry += 1
                WebDriverWhatsappFactory.quit_driver()
                return WebDriverWhatsappFactory.create_driver(retry)
            raise RuntimeError(
                "Não foi possível iniciar o Chrome a pagina esperada"
            )

        return WebDriverWhatsappFactory._driver

    @staticmethod
    def quit_driver():
        """Fecha a instância do WebDriver se estiver ativa."""
        if WebDriverWhatsappFactory._driver is not None:
            WebDriverWhatsappFactory._driver.quit()
            WebDriverWhatsappFactory._driver = None
