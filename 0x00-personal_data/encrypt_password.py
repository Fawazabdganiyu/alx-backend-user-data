#!/usr/bin/env python3
"""Encrypt password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash given password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str, ) -> bool:
    """Validate hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
