#!/usr/bin/env python3
"""Session Database authentication module"""
from datetime import datetime, timedelta
from typing import Optional

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session database authentication class"""

    def create_session(self, user_id: str = None) -> str:
        """Create a new session for a user"""
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> Optional[str]:
        """Get user id for a session"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if not sessions:
            return None
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id
        if session.created_at \
                + timedelta(seconds=self.session_duration) <= datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy a session for a user"""
        if not request:
            return False
        session_id = self.session_cookie(request)

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if not sessions:
            return False

        sessions[0].remove()
        return True
