from flask import Blueprint, request

from app.services.whatsapp_queue import WhatsappQueue
from config.security import token_required

whatsapp_bp = Blueprint("whatsapp", __name__)


# Rota para enviar uma mensagem
@whatsapp_bp.route("/whatsapp", methods=["POST"])
@token_required
def send_message():
    data = request.get_json()

    if data.get("phone_number") is None and data.get("group_id") is None:
        return {
            "status": "erro",
            "mensagem": "Informe o telefone ou grupo",
        }, 400
    elif data.get("message") is None:
        return {
            "status": "erro",
            "mensagem": "Informe a mensagem",
        }, 400

    dto = {
        "phone_number": data.get("phone_number"),
        "group_id": data.get("group_id"),
        "message": data.get("message"),
    }
    WhatsappQueue.put(dto)
    return {"status": "sucesso", "mensagem": "Mensagem enfileirada"}, 201
