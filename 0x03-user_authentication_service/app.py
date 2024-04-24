#!/usr/bin/env python3
"""Flask app module"""
from flask import (
    Flask, jsonify, request, Response,
    abort, make_response, redirect
)

from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> Response:
    """Render home page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Register a user

    form data:
        - email
        - password
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(400, "Email or password is missing")

    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """Login a user

    form data:
        - email
        - password
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(400, "Email or password is missing")
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Response:
    """Logout a user"""
    session_id = request.cookies.get('session_id', '')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Response:
    """Get user profile"""
    session_id = request.cookies.get('session_id', '')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> Response:
    """Get user password reset token

    form data:
        - email
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({'email': email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> Response:
    """Update user password

    form data:
        - email
        - reset_token
        - new_password
    """
    email = request.form.get('email')
    new_password = request.form.get('new_password', '')
    token = request.form.get('reset_token', '')
    try:
        AUTH.update_password(token, new_password)
    except ValueError:
        abort(403)

    return jsonify({'email': email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
