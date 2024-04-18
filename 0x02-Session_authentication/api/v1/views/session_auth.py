#!/usr/bin/env python3
"""Session authentication view module"""
import os

from flask import jsonify, request, make_response

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """POST /api/v1/auth_session/login

    form body:
        - email
        - password

    Returns:
        User object JSON representation on sucess
    """
    from api.v1.app import auth

    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    user_passwd = request.form.get('password')
    if not user_passwd:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(user_passwd):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_auth_logout():
    """DELETE /api/v1/auth_session/logout

    Returns:
        An empty JSON on success, error 404 on failure
    """
    from api.v1.app import auth

    logout = auth.destroy_session(request)
    if not logout:
        abort(404)

    return jsonify({})
