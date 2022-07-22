import os

from flask import Flask, jsonify, make_response
from flask_jwt_simple import JWTManager
from flask_login import LoginManager
from flask_restful import Api

from rich import print
from app.data import db_session
from app.data.user import User
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

        db_session.global_init("app/db/reddit_db.db")
        self.login_manager = LoginManager()
        self.login_manager.init_app(self)
        self.login_manager.login_view = 'users.login'

        self.json_encoder = MyJsonEncoder
        self.users_repo = MemoryUsersRepo()
        self.posts_repo = MemoryPostsRepo()
        self.jwt = JWTManager(self)
        self.api = Api(self)


main_app = MyApp(__name__, static_folder='./../static')
# main_app.config.update(EXPLAIN_TEMPLATE_LOADING=True)


@main_app.jwt.expired_token_loader
def expired_token_callback():
    err_json = {"message": "Expired token"}
    return make_response(jsonify(err_json), 403)  # Можно и 401


@main_app.jwt.invalid_token_loader
@main_app.jwt.unauthorized_loader
def my_inv_unauth_token_callback(why):
    err_json = {"message": why}
    return make_response(jsonify(err_json), 403)  # Можно и 401


@main_app.login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()
