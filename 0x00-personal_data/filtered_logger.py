#!/usr/bin/env python3
"""Definition of filter_datum function"""
import logging
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_msg, self.SEPARATOR)