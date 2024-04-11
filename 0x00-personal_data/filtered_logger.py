#!/usr/bin/env python3
"""Definition of filter_datum function"""
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
