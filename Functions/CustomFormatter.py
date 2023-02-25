import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32m"
    reset = "\x1b[0m"
    log_format = "%(levelname)s: %(asctime)s - %(message)s"

    FORMATS = {
        logging.DEBUG: green + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatte le message de log
        @param record: Enregistrement de log
        @return: Message de log formaté
        """
        log_fmt = self.FORMATS.get(record.levelno)
        icon = ""
        if record.levelno == logging.DEBUG:
            icon = "🐛"
        elif record.levelno == logging.INFO:
            icon = "📝"
        elif record.levelno == logging.WARNING:
            icon = "⚠️"
        elif record.levelno == logging.ERROR:
            icon = "🔥"
        elif record.levelno == logging.CRITICAL:
            icon = "💥"
        log_fmt = icon + " " + log_fmt
        formatter = logging.Formatter(log_fmt, "%Y/%m/%d %H:%M:%S")
        return formatter.format(record)
