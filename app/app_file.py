import os

from flask import Flask, jsonify
from flask_jwt_simple import JWTManager
from flask_restful import Api

from rich import print
from app.data import db_session
from app.resources.posts_repo import MemoryPostsRepo
from app.resources.users_repo import MemoryUsersRepo
from app.tools.my_json_encoder import MyJsonEncoder


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config.from_pyfile('config.py')

        print(f"[bold green]{'=' * 60}[/bold green]",
              f"[i]We are in this dir now:[/i]",
              os.getcwd(),
              f"[bold green]{'=' * 60}[/bold green]",
              sep="\n", end="\n\n")

        db_session.global_init("app/db/TGYM_database.db")

        self.json_encoder = MyJsonEncoder
        self.users_repo = MemoryUsersRepo()
        self.posts_repo = MemoryPostsRepo()
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