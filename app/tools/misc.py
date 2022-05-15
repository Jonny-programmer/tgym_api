from flask import make_response
from flask_jwt_simple import create_jwt

from app.resources.users_repo import User


def make_resp(message, status):
    resp = make_response(message, status)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


def check_keys(dct, keys):
    return all(key in dct for key in keys)


def create_jwt_for_user(user):
    cp_user = {"user": {
        "username": user.username,
        "id": user.id,
    }}
    j_token = {"token": create_jwt(identity=cp_user)}
    return j_token
