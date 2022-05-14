from flask import Flask, jsonify
from flask_jwt_simple import JWTManager
from flask_restful import Api

from resources.posts_repo import InMemoryPostsRepo
from resources.users_repo import SqliteUsersRepo
from tools.my_json_encoder import MyJsonEncoder


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.json_encoder = MyJsonEncoder
        self.users_repo = SqliteUsersRepo("./db/redditclone.db")
        # app.users_repo = InMemoryUsersRepo()
        self.posts_repo = InMemoryPostsRepo()
        self.config.from_pyfile('config.py')
        self.jwt = JWTManager(self)
        self.api = Api(self)


main_app = MyApp(__name__, static_folder='./../static')


@main_app.jwt.expired_token_loader
def expired_token_callback():
    err_json = {"message": "Expired token"}
    return jsonify(err_json), 401


@main_app.jwt.invalid_token_loader
@main_app.jwt.unauthorized_loader
def my_inv_unauth_token_callback(why):
    err_json = {"message": why}
    return jsonify(err_json), 401