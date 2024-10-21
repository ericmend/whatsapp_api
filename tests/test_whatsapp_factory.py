from unittest import mock

import pytest

from app.services.whatsapp_factory import WebDriverWhatsappFactory


# 1. Mock para o `webdriver.Chrome`
@mock.patch("selenium.webdriver.Chrome")
def test_create_driver_initializes_webdriver(mock_chrome):
    # Mock para o driver retornado por `webdriver.Chrome`
    mock_driver = mock.Mock()
    mock_chrome.return_value = mock_driver

    # Mock para `find_elements`, simulando a validação do driver
    mock_driver.find_elements.return_value = [
        mock.Mock()
    ]  # Simula que o elemento foi encontrado

    # Chama o método create_driver
    driver = WebDriverWhatsappFactory.create_driver()

    # Verifica se o driver foi criado e o método `get` foi chamado
    mock_chrome.assert_called_once()
    mock_driver.get.assert_called_once_with("https://web.whatsapp.com")
    assert driver == mock_driver


# 2. Mock do método `_validate_driver` para evitar loops e validação real
@mock.patch(
    "app.services.whatsapp_factory.WebDriverWhatsappFactory._validate_driver",
    return_value=True,
)
@mock.patch("selenium.webdriver.Chrome")
def test_create_driver_valid_driver(mock_chrome, mock_validate_driver):
    # Mock para o driver
    mock_driver = mock.Mock()
    mock_chrome.return_value = mock_driver
    WebDriverWhatsappFactory._driver = None

    # Chama o método create_driver, que deve utilizar o driver mockado
    driver = WebDriverWhatsappFactory.create_driver()

    # Verifica se o driver foi validado e criado corretamente
    mock_validate_driver.assert_called_once()
    mock_driver.get.assert_called_once_with("https://web.whatsapp.com")
    assert driver == mock_driver


# 3. Testando o comportamento do quit_driver
@mock.patch("selenium.webdriver.Chrome")
def test_quit_driver(mock_chrome):
    # Mock para o driver
    mock_driver = mock.Mock()
    WebDriverWhatsappFactory._driver = mock_driver

    # Chama o método quit_driver
    WebDriverWhatsappFactory.quit_driver()

    # Verifica se o driver foi encerrado corretamente
    mock_driver.quit.assert_called_once()
    assert WebDriverWhatsappFactory._driver is None


# 4. Testando a criação do driver com falha na validação (simulando que não
# encontrou o elemento)
@mock.patch(
    "app.services.whatsapp_factory.WebDriverWhatsappFactory._validate_driver",
    return_value=False,
)
@mock.patch("selenium.webdriver.Chrome")
def test_create_driver_retry(mock_chrome, mock_validate_driver):
    # Mock para o driver
    mock_driver = mock.Mock()
    mock_chrome.return_value = mock_driver
    WebDriverWhatsappFactory._driver = None

    # Mock para o quit_driver
    with mock.patch.object(
        WebDriverWhatsappFactory, "quit_driver"
    ) as mock_quit_driver:
        # Chama o método create_driver
        with pytest.raises(
            RuntimeError,
            match="Não foi possível iniciar o Chrome a pagina esperada",
        ):
            WebDriverWhatsappFactory.create_driver(retry=3)

        # Verifica se o driver foi encerrado após a falha
        mock_quit_driver.assert_called_once()
        mock_validate_driver.assert_called()
