#!/usr/bin/env python3
"""Session expiration handler.
"""
import time
import logging
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session expiration handler."""

    def __init__(self):
        """Initialize the session expiration handler."""
        SESSION_DURATION = getenv("SESSION_DURATION", 0)
        try:
            self.SESSION_DURATION = int(SESSION_DURATION)
        except ValueError:
            self.SESSION_DURATION = 0

    def create_session(self, user_id=None):
        """Create a new session with expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_start_time = time.time()
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'start_time': session_start_time
        }
        return session_id

    def user_id_for_session_id(self, session_id: str):
        """Get user ID for a session ID, checking for expiration."""
        if session_id is None or type(session_id) is not str:
            return None
        session_data = self.user_id_by_session_id.get(session_id, None)
        if session_data is None:
            return None
        if self.is_session_expired(session_data['start_time']):
            del self.user_id_by_session_id[session_id]
            return None
        return session_data['user_id']
