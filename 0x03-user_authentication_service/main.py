#!/usr/bin/env python3
"""Integration test module"""
import requests


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/users', data=data)

    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test user login with wrong password"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/sessions', data=data)

    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test user normal login"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/sessions', data=data)

    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}

    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test user profile with unlogged user"""
    resp = requests.get('http://127.0.0.1:5000/profile')

    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test user profile with logged in user"""
    cookies = {'session_id': session_id}
    resp = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)

    assert resp.status_code == 200
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Test a user is logged out"""
    cookies = {'session_id': session_id}
    resp = requests.delete('http://127.0.0.1:5000/sessions', cookies=cookies)

    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test user reset password token"""
    resp = requests.post('http://127.0.0.1:5000/reset_password',
                         data={'email': email})

    assert resp.status_code == 200
    assert email in resp.json().values()

    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test user password update"""
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    resp = requests.put('http://127.0.0.1:5000/reset_password', data=data)

    assert resp.status_code == 200
    assert resp.json() == {'email': email, "message": "Password updated"}


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
