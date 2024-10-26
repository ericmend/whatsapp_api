from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.services.whatsapp_service import send_message


# Fixture para criar um WebDriver simulado
@pytest.fixture
def mock_driver():
    driver = MagicMock()
    return driver


# Testando o envio de mensagem para um grupo
@patch("app.services.whatsapp_factory.WebDriverWhatsappFactory.create_driver")
def test_send_message_group(mock_create_driver, mock_driver):
    mock_create_driver.return_value = mock_driver

    # Simular o comportamento de encontrar o footer e a caixa de input
    mock_footer = MagicMock()
    mock_input_box = MagicMock()

    # O find_elements retorna o footer
    mock_driver.find_elements.return_value = [mock_footer]

    # O find_elements no footer retorna a caixa de mensagem
    mock_footer.find_elements.return_value = [mock_input_box]

    # Dados de entrada simulados
    dto = {"group_id": "12345", "message": "Hello, group!"}

    # Chamando a função para enviar mensagem ao grupo
    send_message(dto)

    # Verificando se o WebDriver foi criado
    mock_create_driver.assert_called_once()

    # Verificando se o link do grupo foi criado e clicado
    mock_driver.execute_script.assert_called()
    mock_driver.find_element.assert_called_with(
        By.ID, f"group_id-{dto['group_id']}"
    )

    # Verificando se a mensagem foi enviada
    assert mock_input_box.send_keys.called
    mock_input_box.send_keys.assert_called_with(dto["message"], Keys.ENTER)


# Testando o envio de mensagem para um número de telefone
@patch("app.services.whatsapp_factory.WebDriverWhatsappFactory.create_driver")
def test_send_message_phone_number(mock_create_driver, mock_driver):
    mock_create_driver.return_value = mock_driver

    # Simular o comportamento de encontrar o footer e a caixa de input
    mock_footer = MagicMock()
    mock_input_box = MagicMock()

    # O find_elements retorna o footer
    mock_driver.find_elements.return_value = [mock_footer]

    # O find_elements no footer retorna a caixa de mensagem
    mock_footer.find_elements.return_value = [mock_input_box]

    # Dados de entrada simulados
    dto = {"phone_number": "5511999999999", "message": "Hello, contact!"}

    # Chamando a função para enviar mensagem ao número
    send_message(dto)

    # Verificando se o WebDriver foi criado
    mock_create_driver.assert_called_once()

    # Verificando se o link do número de telefone foi criado e clicado
    mock_driver.execute_script.assert_called()
    mock_driver.find_element.assert_called_with(By.ID, dto["phone_number"])

    # Verificando se a mensagem foi enviada
    assert mock_input_box.send_keys.called
    mock_input_box.send_keys.assert_called_with(dto["message"], Keys.ENTER)


# Teste para verificar exceções no envio de mensagens
@patch("app.services.whatsapp_factory.WebDriverWhatsappFactory.create_driver")
def test_send_message_error_handling_click(mock_create_driver, mock_driver):
    mock_create_driver.return_value = mock_driver

    # Simulando erro ao clicar no link
    mock_driver.find_element.side_effect = Exception("Erro no clique")

    dto = {"group_id": "12345", "message": "Hello, group!"}

    # Executando e verificando se a exceção foi registrada
    with patch("app.services.whatsapp_service._logger.error") as mock_logger:
        send_message(dto)
        mock_logger.assert_called_once_with(
            "Erro ao executar envio de mensagem: "
            "Erro ao clicar no link do grupo: Erro no clique"
        )


# Teste para verificar exceções no envio de mensagens
@patch("app.services.whatsapp_factory.WebDriverWhatsappFactory.create_driver")
def test_send_message_error_handling_find_elements(
    mock_create_driver, mock_driver
):
    mock_create_driver.return_value = mock_driver

    # Simular o comportamento de encontrar o footer e a caixa de input
    mock_footer = MagicMock()

    # O find_elements retorna o footer
    mock_driver.find_elements.return_value = [mock_footer]

    # Simulando erro na consulta do elemento
    mock_footer.find_elements.side_effect = Exception("Erro no driver")

    dto = {"phone_number": "5511999999999", "message": "Hello, contact!"}

    # Executando e verificando se a exceção foi registrada
    with patch("app.services.whatsapp_service._logger.error") as mock_logger:
        send_message(dto)
        mock_logger.assert_called_once_with(
            "Erro ao executar envio de mensagem: Footer não encontrado."
        )
