import os
from random import choice

from flask import send_from_directory, jsonify, request, render_template, make_response
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask_login import login_required, logout_user, login_user, current_user
from flask_restful import Resource, abort, reqparse
from flask import redirect

from app.app_file import main_app
from app.data import db_session
from app.data.posts import Post
from app.data.user import User
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.tools.misc import create_jwt_for_user


@main_app.route('/')
def root():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    return render_template('index.html', he=current_user, posts=posts)


# @main_app.route('/posts/<int:path>') - страница редактирования
# @main_app.route('/a/<path:path>')
# @main_app.route('/create_post')
# /delete_post/{{ item.id }}


@main_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() or request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(username=form.username.data.lower(),
                    name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    print()
    return render_template('register.html', form=form)


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() or request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data.lower()).first()
        if not user:
            user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data, force=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route("/cookie_test")
def cookie_test():
    button_types = ['primary', 'info', 'danger', 'warning', 'secondary', 'success', 'light', 'dark'
                                                                                             'outline-primary',
                    'outline-info', 'outline-danger', 'outline-warning',
                    'outline-secondary', 'outline-success', 'outline-light', 'outline-dark']
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css'>"
            f"<div align='center'><h1>Вы заходили на эту страницу {visits_count + 1} раз/а</h1>"
            f"<a class='btn btn-{choice(button_types)}' style='align: center;' href='/'>Вернуться домой</a></div>")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24)
    else:
        res = make_response(
            "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css'>"
            "<h1 align='center'>Вы пришли на эту страницу в первый раз за последний день</h1>"
            "<a class='btn btn-primary' style='align: center;' href='/'>Вернуться домой</a>")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24)
    return res


@main_app.errorhandler(404)
def stop_it_man(error):
    return render_template('404.html', error=error)


# Parser for creating a post
post_parser = reqparse.RequestParser()
post_parser.add_argument('category', required=True)
post_parser.add_argument('type', required=True)
post_parser.add_argument('title', required=True)
post_parser.add_argument('text', required=False)
post_parser.add_argument('url', required=False)
# Parser for creating a user
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('password', required=True)


class RegisterRes(Resource):
    def post(self):
        args = user_parser.parse_args()
        created_user = main_app.users_repo.request_create(args["username"], args["password"])
        if not created_user:
            abort(400, message="Duplicated username")
        return create_jwt_for_user(created_user)


class LoginRes(Resource):
    def post(self):
        args = user_parser.parse_args()
        user, error = main_app.users_repo.authorize(args["username"], args["password"])
        if not user:
            abort(400, message=error)
        return create_jwt_for_user(user)


class UserPosts(Resource):
    def get(self, user_login):
        return jsonify(main_app.posts_repo.get_by_username(user_login))


class PostRes(Resource):
    def get(self, post_id):
        post = main_app.posts_repo.get_by_id(post_id)
        print(post)
        return jsonify(post)

    @jwt_required
    def delete(self, post_id):
        result = main_app.posts_repo.request_delete(post_id, User(**get_jwt_identity()))
        if result:
            abort(400, message=result)
        return jsonify({"message": "success"})


class PostListRes(Resource):
    def get(self, **kwargs):
        if "category_name" in kwargs:
            return jsonify(main_app.posts_repo.get_by_category(kwargs["category_name"]))
        posts = main_app.posts_repo.get_all()
        return jsonify(posts)

    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        post = Post(
            category=args.get('category', None),
            title=args.get('title', None),
            text=args.get('text', None),
            url=args.get('url', None),
            type=args.get('type', None),
        )
        print("~~~~This worked!~~~~")
        user_id = get_jwt_identity().get('user').get('id')
        post = main_app.posts_repo.request_create(post, user_id)
        return jsonify(post)


main_app.api.add_resource(RegisterRes, "/api/register")
main_app.api.add_resource(LoginRes, "/api/login")
main_app.api.add_resource(PostListRes, "/api/posts/<category_name>", "/api/posts/")
main_app.api.add_resource(PostRes, "/api/post/<int:post_id>")
main_app.api.add_resource(UserPosts, "/api/user/<user_login>")

# main_app.logger.info('grolsh')


if __name__ == "__main__":
    main_app.run()
