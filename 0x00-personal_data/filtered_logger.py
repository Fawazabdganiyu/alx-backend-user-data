#!/usr/bin/env python3
"""Definition of filter_datum function"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to MySQL"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=user, password=password, host=host, database=db
    )


def main() -> None:
    """Main function"""
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    for row in cursor:
        data = '; '.join([f'{field[0]}={value}'
                          for field, value in zip(cursor.description, row)])
        logger.info(data)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
