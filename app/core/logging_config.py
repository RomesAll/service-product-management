from typing import Literal
from app.core.config import BASE_DIR
import logging

class LevelFilter(logging.Filter):

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

class LoggingSettings:

    def __init__(self, logger_name: str, level: str | int):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

    @staticmethod
    def create_formatter(format: str = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"):
        return logging.Formatter(format)

    def create_handler_console(self, level: str | int, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.create_formatter(formatter))
        handler.addFilter(LevelFilter(level))
        self.logger.addHandler(handler)

    def create_handler_file(self, filename: str, filemode: str, level: str | int, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        handler = logging.FileHandler(filename, filemode, delay=True)
        handler.setLevel(level)
        handler.setFormatter(self.create_formatter(formatter))
        handler.addFilter(LevelFilter(level))
        self.logger.addHandler(handler)

logging_setup = LoggingSettings(logger_name="app", level="DEBUG")
logging_setup.create_handler_console(level=logging.DEBUG)
logging_setup.create_handler_file(filename=f'{BASE_DIR}/app/logs/info.log', filemode='a', level=logging.INFO)
logging_setup.create_handler_file(filename=f'{BASE_DIR}/app/logs/warning.log', filemode='a', level=logging.WARNING)
logging_setup.create_handler_file(filename=f'{BASE_DIR}/app/logs/error.log', filemode='a', level=logging.ERROR)