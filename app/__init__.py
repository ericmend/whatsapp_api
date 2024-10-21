from flask import Flask

from config.environment import Environment

app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Environment)

    from .routes_whatsapp import whatsapp_bp

    app.register_blueprint(whatsapp_bp)

    from .routes_health_check import health_bp

    app.register_blueprint(health_bp)

    return app
