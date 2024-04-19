#!/usr/bin/env python3
"""Session Database authentication module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session database authentication class"""

    def create_session(self, user_id=None):
        """Create a new session for a user"""
        session_id = super().create_session(user_id)
        user_id = self.user_id_by_session_id(session_id)
        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id for a session"""
        pass

    def destroy_session(self, request=None):
        """Destroy a session for a user"""
        pass
