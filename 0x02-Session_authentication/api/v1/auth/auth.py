#!/usr/bin/env python3
"""API Authentication module"""
import os

from flask import request
from typing import List, TypeVar, Optional


class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine the routes that require authentication
        """
        if not path or not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'
        # Consider when excluded_paths = ["/api/v1/stat*"]
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                excluded_path = excluded_path[:-1]
                if excluded_path in path:
                    return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Get authorization content
        """
        if not request or 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user information
        """
        return None

    def session_cookie(self, request=None) -> Optional[str]:
        """Get a cookie value from a request
        """
        if request is None:
            return None

        cookies_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookies_name)
