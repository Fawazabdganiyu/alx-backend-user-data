#!/usr/bin/env python3
"""API Authentication module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """Determine the routes that require authentication
        """
        if not path or not excluded_path:
            return True

        path = path if path.endswith('/') else path + '/'
        return path not in excluded_path

    def authorization_header(self, request=None) -> str:
        """Get authorization
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user information
        """
        return None
