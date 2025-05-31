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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.

    :param hashed_password: The hashed password to check against.
    :param password: The plain text password to verify.
    :return: True if the password matches, False otherwise.
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
