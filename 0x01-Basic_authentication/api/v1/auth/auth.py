#!/usr/bin/env python3
"""API Authentication module"""
from flask import request
from typing import List


class Auth:
    """Authentication class"""
    def required_auth(self, path: str, excluded_path: List[str]) -> bool:
        """Determine the routes that require authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Get authorization
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user information
        """
        return None
