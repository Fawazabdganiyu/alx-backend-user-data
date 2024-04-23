#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request, Response, abort

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
