#!/usr/bin/env python3
# type: ignore
"""Session database management Authentication."""
import logging
from datetime import datetime, timedelta
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
        try:
            session = UserSession.get(UserSession.session_id == session_id)
            if session and session.created_at + timedelta(seconds=self.session_duration) > datetime.now():
                return session.user_id
        except UserSession.DoesNotExist:
            return None
        except Exception as e:
            logging.error(f"Error retrieving user ID for session: {e}")
            return None
        return None

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
