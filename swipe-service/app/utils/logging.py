import logging

from infrastructure.middleware import get_correlation_id


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        return True


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | corr_id=%(correlation_id)s | %(name)s | %(message)s"
    )

    # console_handler = logging.StreamHandler()  # best practice for ELK
    # console_handler.setFormatter(formatter)
    # console_handler.addFilter(CorrelationIdFilter())
    # logger.addHandler(console_handler)

    file_handler = logging.FileHandler("app.log")  # for local development
    file_handler.setFormatter(formatter)
    file_handler.addFilter(CorrelationIdFilter())

    logger.addHandler(file_handler)
