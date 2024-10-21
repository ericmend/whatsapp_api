from flask import Blueprint

health_bp = Blueprint("health", __name__)


@health_bp.route("/health_check", methods=["GET"])
def health_check():
    return {}, 200
