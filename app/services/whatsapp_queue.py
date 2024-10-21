import queue
import threading

from app.services import whatsapp_service


class WhatsappQueue:

    # Cria uma fila para armazenar as requisições
    _task_queue: queue.Queue = queue.Queue()
    _worker_thread: threading.Thread

    @staticmethod
    def put(data):
        WhatsappQueue._task_queue.put(data)

    @staticmethod
    def _process_tasks():
        """Função para processar as tarefas na fila."""
        while True:
            # Aguarda uma tarefa na fila
            data = WhatsappQueue._task_queue.get()
            if data is not None:
                whatsapp_service.send_message(data)
            WhatsappQueue._task_queue.task_done()

    @staticmethod
    def start():
        # Inicia a thread que processa as tarefas
        WhatsappQueue._worker_thread = threading.Thread(
            target=WhatsappQueue._process_tasks, daemon=True
        )
        WhatsappQueue._worker_thread.start()
