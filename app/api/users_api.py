from flask import jsonify
from flask_restful import Resource, reqparse, abort

from app.app_file import main_app
from app.tools.misc import create_jwt_for_user

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)


class RegisterRes(Resource):
    def post(self):
        args = parser.parse_args()
        created_user = main_app.users_repo.request_create(args["username"], args["password"])
        if not created_user:
            abort(400, message="Duplicated username")
        return create_jwt_for_user(created_user)


class LoginRes(Resource):
    def post(self):
        args = parser.parse_args()
        user, error = main_app.users_repo.authorize(args["username"], args["password"])
        if not user:
            abort(400, message=error)
        return create_jwt_for_user(user)


class UserPosts(Resource):
    def get(self, user_login):
        return jsonify(main_app.posts_repo.get_by_username(user_login))