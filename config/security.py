import jwt
from flask import request, jsonify, abort
from config.environment import Environment

env = Environment()

def token_required(f):
    """Decorador para validar o token JWT."""
    def decorator(*args, **kwargs):
        token = None
        # Verifica se o token está no cabeçalho da requisição
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Espera o formato "Bearer <token>"

        if not token:
            return jsonify({"status": "erro", "mensagem": "Token não fornecido"}), 401

        try:
            # Decodifica o token usando a chave secreta
            data = jwt.decode(token, env.SECRET_KEY, algorithms=[env.JWT_ALGORITHM])
            # Aqui você pode adicionar lógica para validar o usuário, se necessário
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "erro", "mensagem": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "erro", "mensagem": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorator
