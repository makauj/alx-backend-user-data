#!/usr/bin/env python3
"""Session database management Authentication.
"""
import logging
from datetime import datetime
from api.v1.auth.session_exp_auth import load_from_file
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class to manage session database authentication."""

    def create_session(self, user_id=None):
        """Create a session for a user."""
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        try:
            UserSession.create(user_id=user_id, session_id=session_id,
                               created_at=datetime.now())
        except Exception as e:
            logging.error(f"Error creating session in DB: {e}")
            return None
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID for a given session ID."""
        if session_id is None:
            return None
        UserSession = load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        if self.is_session_expired(user_session.created_at):
            self.destroy_session(session_id)
            return None
        return user_session.user_id

    def destroy_session(self, session_id=None):
        """Destroy a session."""
        if session_id is None:
            return False
        try:
            UserSession.delete().where(UserSession.session_id == session_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error destroying session in DB: {e}")
            return False
