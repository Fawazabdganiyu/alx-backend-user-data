#!/usr/bin/env python3
"""Definition of filter_datum function"""
import logging
import re
from typing import Sequence

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: Sequence, redaction: str, message: str, separator: str
) -> str:
    """Replace occurrence of certain field value"""
    for field in fields:
        message = re.sub(fr"({field}=[^{separator}]+)",
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log record"""
        log_msg: str = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return logger instance"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(handler)

    return logger
