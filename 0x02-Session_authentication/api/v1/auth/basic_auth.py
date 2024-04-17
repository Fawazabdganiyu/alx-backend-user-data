#!/usr/bin/env python3
"""Basic Authentication Module"""
from base64 import b64decode
import binascii
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


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
        except Exception:
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
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Retrieve User instance by its credentials
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the user for a request
        """
        auth_str = self.extract_base64_authorization_header(
            self.authorization_header(request))
        decoded_str = self.decode_base64_authorization_header(auth_str)
        email, password = self.extract_user_credentials(decoded_str)

        return self.user_object_from_credentials(email, password)
