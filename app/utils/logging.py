import logging
import queue
from logging.handlers import QueueHandler, QueueListener


def setup_logging_queue() -> None:
    # TODO вынести настройки логирования в config файл
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s <> %(message)s')

    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)  # Non-blocking handler.
    queue_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    root.addHandler(queue_handler)
    root.addHandler(console_handler)

    queue_listener = QueueListener(log_queue)
    queue_listener.start()
