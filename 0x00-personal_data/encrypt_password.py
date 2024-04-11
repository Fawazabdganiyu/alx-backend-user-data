#!/usr/bin/env python3
"""Encrypt password module"""
import bcrypt


def hash_password(password):
    """Hash given password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
