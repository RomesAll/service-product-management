from typing import Literal
import logging

class LoggingSettings:
    def __init__(self, logger_name: str = 'app', level: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"] = logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

    @staticmethod
    def create_formatter(format: str = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"):
        return logging.Formatter(format)

    def get_logger(self):
        return self.logger

    def create_handler_console(self, level = logging.DEBUG, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.create_formatter(formatter))
        self.logger.addHandler(handler)

    def create_handler_file(self, filename: str, filemode: str, level = logging.DEBUG, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        handler = logging.FileHandler(filename, mode=filemode)
        handler.setLevel(level)
        handler.setFormatter(self.create_formatter(formatter))
        self.logger.addHandler(handler)

logging_setup = LoggingSettings(logger_name="app", level="DEBUG")
logging_setup.create_handler_console(level=logging.DEBUG)
logging_setup.create_handler_file(filename='info.log', filemode='a', level=logging.INFO)
logging_setup.create_handler_file(filename='warning.log', filemode='a', level=logging.WARNING)
logging_setup.create_handler_file(filename='error.log', filemode='a', level=logging.ERROR)