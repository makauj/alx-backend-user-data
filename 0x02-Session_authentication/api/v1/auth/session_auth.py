#!/usr/bin/env python3
# type: ignore
"""Session Authentication Middleware"""
from api.v1.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    Class SessionAuth that inherits from Auth
    Creating a new authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id=None):
        """
        Creates a new session ID for a user
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str):
        """Session ID to User ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Current user based on session ID
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Logout function that deletes the session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
