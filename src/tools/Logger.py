import logging

class Logger:
    def __init__(self, name, level=logging.DEBUG):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self._logger.addHandler(handler)

    def debug(self, message):
        self._logger.debug(message)

    def info(self, message):
        self._logger.info(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)