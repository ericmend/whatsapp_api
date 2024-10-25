from app import create_app
from app.services.whatsapp_factory import WebDriverWhatsappFactory
from app.services.whatsapp_queue import WhatsappQueue
from config.environment import Environment

import logging

env = Environment()
_logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

WebDriverWhatsappFactory.create_driver()
WhatsappQueue.start()
app = create_app()

if __name__ == '__main__':
    _logger.info("started")
    from waitress import serve
    serve(app, host="0.0.0.0", port=env.APP_PORT)