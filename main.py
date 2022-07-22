import sys
from datetime import datetime
from random import choice

from flask import jsonify, request, render_template, make_response, flash
from flask import redirect
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask_login import login_required, logout_user, login_user, current_user
from flask_restful import Resource, abort, reqparse
from waitress import serve

from app.app_file import main_app
from app.data import db_session
from app.data.posts import Post
from app.data.user import User
from app.forms.create_post import CreatePostForm
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.tools.misc import create_jwt_for_user


@main_app.route('/')
def root():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    categories = []
    show_buttons = []
    for post in posts:
        categories.append(post.category)
        if current_user.is_authenticated and current_user == post.author:
            show_buttons.append(1)
        else:
            show_buttons.append(0)
    return render_template('main.html', he=current_user, posts=posts, show_buttons=show_buttons,
                           categories=categories)


@main_app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit() or request.method == 'POST':
        db_sess = db_session.create_session()
        post = Post(
            title=form.title.data,
            text=form.content.data,
            is_private=form.is_private.data,
            created=datetime.now(),
            category=form.category.data
        )
        current_user.posts.append(post)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('create_post.html', form=form, title="Добавить новость")


@main_app.route('/posts/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if not current_user.is_authenticated:
        flash("You must log in to see that", 'warning')
        return redirect('/')
    form = CreatePostForm()
    if request.method == "GET":
        post = main_app.posts_repo.get_by_id(id)
        if post:
            form.title.data = post.title
            form.content.data = post.text
            form.category.data = post.category
            form.is_private.data = post.is_private
        else:
            abort(404)
    if form.validate_on_submit() or request.method == "POST":
        db_sess = db_session.create_session()
        post = db_sess.query(Post).filter(Post.id == id, Post.author == current_user).first()
        if post:
            post.title = form.title.data
            post.text = form.content.data
            post.category = form.category.data
            post.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('create_post.html', title='Редактирование поста', form=form)


@main_app.route('/a/<category_name>')
def show_all_by_cat(category_name):
    posts = main_app.posts_repo.get_by_category(category_name)
    show_buttons = []
    for post in posts:
        if current_user.is_authenticated and current_user == post.author:
            show_buttons.append(1)
        else:
            show_buttons.append(0)
    return render_template('category_posts.html', category=category_name,
                           he=current_user, posts=posts, show_buttons=show_buttons)


@main_app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id, Post.author == current_user).first()
    if post:
        db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@main_app.route('/users/<int:id>', defaults={'nickname': None}, methods=['GET', 'POST'])
@main_app.route('/users/<nickname>', defaults={'id': None}, methods=['GET', 'POST'])
def profile(id=None, nickname=None):
    form = RegisterForm()
    user = main_app.users_repo.get_by_id(id)
    if not user:
        user = main_app.users_repo.get_by_username(nickname)
        if not user:
            abort(404)
    if form.validate_on_submit() or request.method == 'POST':
        print("Ooops....")
        sys.exit(1)
    return render_template('profile.html', he=current_user, user=user, form=form)


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
            f"<a class='btn btn-{choice(button_types)}' style='align: center;' href='/'>Вернуться домой</a></div>"
            )
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24)
    else:
        res = make_response(
            "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css'>"
            "<h1 align='center'>Вы пришли на эту страницу в первый раз за последний день</h1>"
            "<a class='btn btn-primary' style='align: center;' href='/'>Вернуться домой</a>"
            )
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24)
    return res


@main_app.route('/about')
def about():
    return render_template('about.html', he=current_user)


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
user_parser.add_argument('name', required=True)
user_parser.add_argument('surname', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)


class RegisterRes(Resource):
    def post(self):
        args = user_parser.parse_args()
        created_user = main_app.users_repo.request_create(
            args["username"], args['name'], args['surname'], args['email'], args["password"])
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

if __name__ == "__main__":
    main_app.run(host="0.0.0.0", port=5000)
    # main_app.run()
    # serve(main_app)
