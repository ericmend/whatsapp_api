import time
from unittest.mock import patch

import pytest

from app.services.whatsapp_queue import WhatsappQueue


@pytest.fixture
def clear_queue():
    """Fixture para limpar a fila antes de cada teste"""
    while not WhatsappQueue._task_queue.empty():
        WhatsappQueue._task_queue.get_nowait()


# Agora o patch é aplicado no módulo whatsapp_service
@patch("app.services.whatsapp_service.send_message")
def test_put_message_in_queue(mock_send_message, clear_queue):
    # Inicializa o processamento (isso inicia a thread)
    WhatsappQueue.start()

    # Coloca um dado na fila
    message_data = {"to": "+1234567890", "message": "Hello!"}
    WhatsappQueue.put(message_data)

    # Dá um tempo para a thread processar a fila
    time.sleep(1)

    # Verifica se o método mockado foi chamado corretamente
    mock_send_message.assert_called_once_with(message_data)

    # Verifica se a fila está vazia depois de processada
    assert WhatsappQueue._task_queue.empty()


@patch("app.services.whatsapp_service.send_message")
def test_queue_task_done(mock_send_message, clear_queue):
    # Inicializa o processamento (isso inicia a thread)
    WhatsappQueue.start()

    # Coloca um dado nulo na fila
    WhatsappQueue.put(None)

    # Dá um tempo para a thread processar a fila
    time.sleep(1)

    # Verifica se o método mockado foi chamado corretamente
    mock_send_message.assert_not_called()

    # Verifica se a fila está vazia
    assert WhatsappQueue._task_queue.empty()
