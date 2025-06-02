#!/usr/bin/env python3
"""Session Authentication Middleware"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login route for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User.search({'email': email})
    if not user or not user[0].is_valid_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    SESSION_NAME = getenv("SESSION_NAME")
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logout route for session authentication"""
    if not auth.destroy_session(request):
        return jsonify({"error": "not logged in"}), 404
    return jsonify({}), 200
