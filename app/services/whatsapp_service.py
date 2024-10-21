import logging
import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.services.whatsapp_factory import WebDriverWhatsappFactory

_logger = logging.getLogger(__name__)
_lock = threading.Lock()  # Criação do lock


def create_group_link_element(driver, group_id) -> str:
    """Cria e insere um link de grupo no DOM da página."""
    id = f"group_id-{group_id}"
    script = f"""
        const lnk = document.createElement("a");
        const lnk_node = document.createTextNode("{id}");
        lnk.appendChild(lnk_node);
        lnk.setAttribute("id", "{id}");
        lnk.setAttribute("href", "https://chat.whatsapp.com/{group_id}");
        const element1 = document.getElementById("pane-side");
        element1.appendChild(lnk);
    """
    driver.execute_script(script)
    return id


def create_phone_number_link_element(driver, phone_number) -> str:
    """Cria e insere um link de grupo no DOM da página."""
    id = f"{phone_number}"
    script = f"""
        const lnk = document.createElement("a");
        const lnk_node = document.createTextNode("{id}");
        lnk.appendChild(lnk_node);
        lnk.setAttribute("id", "{id}");
        lnk.setAttribute("href","https://api.whatsapp.com/send?phone={id}");
        const element1 = document.getElementById("pane-side");
        element1.appendChild(lnk);
    """
    driver.execute_script(script)
    return id


def remove_link_element(driver, id):
    """Remove o link previamente inserido no DOM."""
    script = f"""
        const element = document.getElementById("{id}");
        if (element) {{
            element.parentNode.removeChild(element);
        }}
    """
    driver.execute_script(script)


def click_link_by_id(driver, id):
    """Clica no link inserido."""
    try:
        link_element = driver.find_element(By.ID, id)
        link_element.click()
    except Exception as e:
        raise Exception(f"Erro ao clicar no link do grupo: {e}")


def send_message_in_chat(driver, message):
    """Envia a mensagem no chat ativo."""
    try:
        time.sleep(2)  # Garantir que o chat carregue
        footers = driver.find_elements(By.CSS_SELECTOR, "footer._ak1i")
        if footers:
            footer = footers[0]
            input_box = footer.find_elements(
                By.CSS_SELECTOR, ".selectable-text.copyable-text"
            )
            if input_box:
                message_box = input_box[0]
                message_box.click()
                message_box.send_keys(message, Keys.ENTER)
                _logger.info("Mensagem enviada com sucesso.")
            else:
                raise Exception("Caixa de mensagem não encontrada.")
        else:
            raise Exception("Footer não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao enviar a mensagem: {e}")


def execute_send_message_group(dto):
    """
    Executa o fluxo de envio de mensagem no WhatsApp Web
    para o grupo informado.
    """
    driver = WebDriverWhatsappFactory.create_driver()
    try:
        id = create_group_link_element(driver, dto["group_id"])
        click_link_by_id(driver, id)
        remove_link_element(driver, id)
        send_message_in_chat(driver, dto["message"])
    except Exception as e:
        _logger.error(f"Erro ao executar envio de mensagem: {e}")


def execute_send_message_phone_number(dto):
    """
    Executa o fluxo de envio de mensagem no WhatsApp Web
    para o numero informado.
    """
    driver = WebDriverWhatsappFactory.create_driver()
    try:
        id = create_phone_number_link_element(driver, dto["phone_number"])
        click_link_by_id(driver, id)
        remove_link_element(driver, id)
        send_message_in_chat(driver, dto["message"])
    except Exception as e:
        _logger.error(f"Erro ao executar envio de mensagem: {e}")


def send_message(dto):
    """
    Controla o fluxo de envio de mensagem com locking
    para garantir exclusividade.
    """
    with _lock:
        if dto.get("group_id") is not None:
            execute_send_message_group(dto)
            return
        execute_send_message_phone_number(dto)
