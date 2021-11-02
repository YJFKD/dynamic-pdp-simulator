import logging
import sys


class LoggingEngine:
    def __init__(self, level="debug", contents=None, logger_name=None):
        self.logging_level_dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }

        logging_level = self.logging_level_dict.get(level.lower(), logging.DEBUG)

        if contents is None:
            contents = ["asctime", "levelname", "funcName", "lineno", "message"]

        if logger_name is None:
            logger_name = 'logging_engine'

        logging_fmt = "%(asctime)s [%(filename)-15s | %(lineno)d] %(levelname)s: %(message)s"
        # logging_fmt = " - ".join([f"%({content})s" for content in contents])

        logger = logging.getLogger(logger_name)
        logger.setLevel(level=logging_level)
        formatter = logging.Formatter(logging_fmt)
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger
        self.logger_name = logger_name
        self.handlers = {}
        self.formatter = formatter

        self.import_log_funcs()

    def import_log_funcs(self):
        log_funcs = ['debug', 'info', 'warning', 'error', 'critical', 'exception']
        for func_name in log_funcs:
            func = getattr(self.logger, func_name)
            setattr(self, func_name, func)

    def add_file_output(self, filename: str, level='info', mode="w"):
        if filename not in self.handlers:
            handler = logging.FileHandler(filename, mode=mode, encoding='UTF-8')
            handler.setFormatter(self.formatter)
            handler.setLevel(self.logging_level_dict.get(level.lower(), logging.DEBUG))
            self.handlers[filename] = handler
            self.logger.addHandler(handler)

    def remove_file_handler(self, file_path):
        if file_path in self.handlers:
            self.logger.removeHandler(self.handlers.get(file_path))

    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def critical(self, msg: str):
        pass

    def exception(self, msg: str):
        pass


logger = LoggingEngine(logger_name="glob_logging_engine",
                       level="info")


def test_log():
    log = LoggingEngine(level="debug",
                        contents=["asctime", "levelname", "filename", "lineno", "funcName", "message"])

    log.info("Hello World!")