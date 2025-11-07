import logging
from collections import deque

class AppLogger:
    def __init__(self, name="AppLogger", filename="app.log", maxlen =50):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(filename, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self._debug_log = deque(maxlen=maxlen)
        self._rag_log = deque(maxlen=maxlen)
        self._kelvin_log = deque(maxlen=maxlen)
    

    def update_debug_log(self, text):
        self._debug_log.append(str(text))
        self.logger.debug(text)

    def clear_rag_log(self):
        self._rag_log.clear()
        self.logger.info("RAG log cleared")
    
    def update_rag_log(self, text):
        self._rag_log.append(str(text))
        self.logger.info(f"RAG: {text}")

    def update_kelvin_log(self, text):
        self._kelvin_log.append(str(text))
        self.logger.debug(text)

    def log(self, level, category, text):
        msg = f"[{category}] {text}"
        getattr(self.logger, level, self.logger.info)(msg)

       