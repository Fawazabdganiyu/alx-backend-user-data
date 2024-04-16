#!/usr/bin/env python3
"""Basic Authentication Module"""
import binascii

from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """BasicAuth class definition
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """Extract base64 part of the authorization header
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """Decode base64 string from authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_byte = b64decode(base64_authorization_header)
            decoded_str = decoded_byte.decode('utf-8')
        except binascii.Error:
            return None

        return decoded_str

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user credentials"""
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password
