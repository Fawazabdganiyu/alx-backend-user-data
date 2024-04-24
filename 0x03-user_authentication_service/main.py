#!/usr/bin/env python3
"""Integration test module"""
import requests


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/users', data=data)

    assert resp.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test user login with wrong password"""
    pass

def log_in(email: str, password: str) -> str:
    """Test user normal login"""
    pass

def profile_unlogged() -> None:
    """Test user profile with unlogged user"""
    pass

def profile_logged(session_id: str) -> None:
    """Test user profile with logged in user"""
    pass
def log_out(session_id: str) -> None:
    """Test a user is logged out"""
    pass

def reset_password_token(email: str) -> str:
    """Test user reset password token"""
    pass

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test user password update"""
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)