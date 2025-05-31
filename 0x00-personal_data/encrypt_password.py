#!/usr/bin/env python3
"""
A hash_password function that expects one string argument name `password`
and returns a salted, hashed password, which is a byte string.
It uses the `bcrypt` library to hash the password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    :param password: The password to hash.
    :return: A salted, hashed password as a byte string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
