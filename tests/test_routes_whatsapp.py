import json

import pytest

from app import create_app
from app.services.whatsapp_queue import WhatsappQueue

BEARER = (
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30."
    "7sEXtx7-by8WsMR4Mr1PvHrQR6EjmctKeVEAqF5CoBw"
)


@pytest.fixture
def client():
    app_created = create_app()
    response_client = app_created.test_client()
    app_created.testing = True

    return response_client


def test_send_message(client):
    new_message = {
        "phone_number": "+1234567890",
        "group_id": "ABCDEF",
        "message": "Olá, mundo!",
    }
    response = client.post(
        "/whatsapp",
        data=json.dumps(new_message),
        content_type="application/json",
        headers={"Authorization": BEARER},
    )
    assert response.status_code == 201

    # Verifica se a mensagem foi adicionada à fila
    assert len(WhatsappQueue._task_queue.queue) == 1

    dto = WhatsappQueue._task_queue.get()
    assert dto["phone_number"] == "+1234567890"
    assert dto["group_id"] == "ABCDEF"
    assert dto["message"] == "Olá, mundo!"

    # Limpa a fila (opcional)
    WhatsappQueue._task_queue.queue.clear()


def test_empty_data(client):
    data = {}
    response = client.post(
        "/whatsapp",
        json=data,
        headers={"content_type": "application/json", "Authorization": BEARER},
    )
    assert response.status_code == 400


def test_invalid_data(client):
    data = {
        "phone_number": "+1234567890",
        "group_id": "ABCDEF",
        "message": None,
    }
    response = client.post(
        "/whatsapp",
        json=data,
        headers={"content_type": "application/json", "Authorization": BEARER},
    )
    assert response.status_code == 400
