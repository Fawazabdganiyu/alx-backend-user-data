#!/usr/bin/env python3
"""Session Expiration Authentication module"""
import os
from datetime import datetime, timedelta
from typing import Optional

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class"""
    def __init__(self):
        """Initialise Session Expiration"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Optional[str]:
        """"Create a new session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """Get user id for a session"""
        session_dict = super().user_id_for_session_id(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict['user_id']
        if not session_dict.get('created_at'):
            return None
        if session_dict.get('created_at') \
                + timedelta(seconds=self.session_duration) <= datetime.now():
            return None

        return session_dict['user_id']
