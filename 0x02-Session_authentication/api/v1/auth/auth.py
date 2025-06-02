#!/usr/bin/env python3
# type: ignore
"""manage API authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        """Returns True if the path requires authentication, False otherwise"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure trailing slash consistency
        if not path.endswith("/"):
            path += "/"

        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                # Match prefix if wildcard is used
                if path.startswith(ex_path[:-1]):
                    return False
            else:
                # Normalize for exact matches
                if not ex_path.endswith("/"):
                    ex_path += "/"
                if path == ex_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from the request"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> None:
        """Return the current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """Return the session cookie from the request"""
        if request is None:
            return None
        SESSION_NAME = getenv("SESSION_NAME")
        if SESSION_NAME is None:
            return None
        return request.cookies.get(SESSION_NAME)
