#!/usr/bin/env python3
"""Session Authentication module"""
from uuid import uuid4

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for a current user
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get a user_id for a session
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
