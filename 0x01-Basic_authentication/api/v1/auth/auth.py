#!/usr/bin/env python3
"""manage API authentication"""
from flask import request


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Check if the path requires authentication"""
        if path is None or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from the request"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> None:
        """Return the current user"""
        return None
