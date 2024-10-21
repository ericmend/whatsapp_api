from app import create_app
from app.services.whatsapp_factory import WebDriverWhatsappFactory
from app.services.whatsapp_queue import WhatsappQueue
import logging

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
    app.run()