#!/usr/bin/env python3
"""Falsk App"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello():
    """Return a simple greeting"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already redistered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def log_in():
    """Log in a user and create a session"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        return jsonify({"message": "email or password missing"}), 400

    if not AUTH.valid_login(email, password):
        return jsonify({"message": "invalid credentials"}), 401

    session_id = AUTH.create_session(email)
    response = jsonify(
        {"email": email,
         "message": "logged in"}).set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def log_out():
    """Log out a user and destroy the session"""
    session_id = request.cookies.get('session_id', None)

    if not session_id:
        abort(403)

    user = AUTH._db.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Get the profile of the logged-in user"""
    session_id = request.cookies.get('session_id', None)

    if not session_id:
        abort(403)

    user = AUTH._db.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Generate a reset password token for a user"""
    try:
        email = request.form['email']
    except KeyError:
        return jsonify({"message": "email missing"}), 400

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        return jsonify({"message": "email not registered"}), 403

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update the password for a user using a reset token"""
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError as e:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
