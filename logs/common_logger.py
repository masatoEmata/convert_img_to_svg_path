import logging
from logging import getLogger, FileHandler, Formatter
# https://sakusaku-techs.com/python/logging/

class Log:

    def __init__(self):

        def app_log_handler() -> None:
            l = getLogger('APP')
            formatter = Formatter(
                '%(asctime)s <%(levelname)s> : %(message)s')
            fileHandler = FileHandler('./logs/APP.log', mode='a')
            fileHandler.setFormatter(formatter)
            l.setLevel(logging.INFO)
            l.addHandler(fileHandler)

        def sql_log_handler() -> None:
            l = getLogger('SQL')
            formatter = Formatter(
                '%(asctime)s <%(levelname)s> : %(message)s')
            fileHandler = FileHandler('./logs/SQL.log', mode='a')
            fileHandler.setFormatter(formatter)
            l.setLevel(logging.INFO)
            l.addHandler(fileHandler)

        def error_log_handler() -> None:
            l = getLogger('ERROR')
            formatter = Formatter(
                '%(asctime)s <%(levelname)s> : %(message)s')
            fileHandler = FileHandler('./logs/ERROR.log', mode='a')
            fileHandler.setFormatter(formatter)
            l.setLevel(logging.INFO)
            l.addHandler(fileHandler)

        app_log_handler()
        sql_log_handler()
        error_log_handler()
        Log.__instance = self

    def app_info(self, msg) -> None:
        log = getLogger('APP')
        log.info(msg)

    def sql_info(self, msg) -> None:
        log = getLogger('SQL')
        log.info(msg)

    def all_error(self, msg) -> None:
        log = getLogger('ERROR')
        log.error(msg)
