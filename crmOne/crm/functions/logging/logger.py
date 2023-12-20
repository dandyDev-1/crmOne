import logging
from pythonjsonlogger import jsonlogger
import settings
import inspect


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(settings.APP_NAME)
        self.logger.setLevel(logging.DEBUG)

        self.dbLogger = logging.getLogger("sqlalchemy.engine")
        self.dbLogger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(settings.APP_LOG)
        file_handler.setLevel(logging.INFO)

        dbFileHandler = logging.FileHandler(settings.DATABASE_LOG)
        dbFileHandler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = jsonlogger.JsonFormatter(
            fmt="%(levelname)s %(asctime)s %(module) %(name) %(message)",
            datefmt="%Y-%m-%d %H:%M.%S",
            json_ensure_ascii=True,
            json_indent=4
        )

        file_handler.setFormatter(formatter)
        dbFileHandler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.dbLogger.addHandler(dbFileHandler)

    def log(self, message, severity=""):
        frame = inspect.currentframe().f_back
        function_name = frame.f_code.co_name
        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno

        extra_info = {
            'FuncName': function_name,
            'FileName': file_name.split('/')[-1],
            'LineNo': line_number
        }

        if not severity or severity == "info":
            self.logger.info(message, extra=extra_info)
        elif severity == "debug":
            self.logger.debug(message, extra=extra_info)
        elif severity == "warning":
            self.logger.warning(message, extra=extra_info)
        elif severity == "error":
            self.logger.error(message, extra=extra_info)
        elif severity == "critical":
            self.logger.critical(message, extra=extra_info)
