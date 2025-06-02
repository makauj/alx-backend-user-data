#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication class that inherits from Auth"""

    def __init__(self, username, password):
        """Initialize with username and password"""
        self.username = username
        self.password = password

    def authenticate(self, provided_username, provided_password):
        """Check if provided credentials match the stored ones"""
        return (provided_username == self.username and
                provided_password == self.password)

    def __str__(self):
        """Return a string representation of the authentication method"""
        return f"BasicAuth(username={self.username})"

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header"""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return (authorization_header.split(" ")[1]
                if " " in authorization_header else None)

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode the Base64 encoded Authorization header"""
        import base64
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> tuple:
        """
        Extract user credentials from the decoded Base64 Authorization header
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_info = decoded_base64_authorization_header.split(':', 1)
        return user_info[0], user_info[1] if len(user_info) > 1 else None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> tuple[str, str] | tuple[None, None]:
        """
        Extracts user email and password from the
        Base64 decoded authorization header.

        Returns:
            A tuple of (email, password), or (None, None) if input is invalid.
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar['User']:
        """Return a User object based on the provided credentials"""
        from models.user import User
        if not user_email or not user_pwd:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> str:
        """Return the current user based on the request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if not base64_auth_header:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if not decoded_auth_header:
            return None
        username, password = self.extract_user_credentials(
            decoded_auth_header)
        if not username or not password:
            return None
        if self.authenticate(username, password):
            return username
        return None
