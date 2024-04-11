#!/usr/bin/env python3
"""Definition of filter_datum function"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Replace occurrence of certain field value

    Args:
        fields (List[str]): A list of strings for all fields to obfuscate
        redaction (str): A string to obfuscate the field with
        message (str): A string representing the log line
        separator (str): A string that separate all the fields
                         in the log line (message)

    Returns:
        str: The log message obfuscated
    """
    for field in fields:
        if field in message:
            obfuscated_msg = re.sub(fr"({field}=[^{separator}]+)",
                                    f'{field}={redaction}', message)
            message = obfuscated_msg
    return message
