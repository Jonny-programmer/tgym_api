import os

from fastapi.encoders import jsonable_encoder
from flask import send_from_directory, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from app.app_file import main_app
from app.data.posts import Post
from app.data.user import User
from app.tools.misc import create_jwt_for_user


@main_app.route('/', defaults={'path': ''}, methods=['GET'])
@main_app.route('/u/<path:path>')
@main_app.route('/a/<path:path>')
def root(path):
    print("Here we go, maaaaaan")
    path = os.path.join(os.getcwd(), "static")
    print(path)
    return send_from_directory(path, "index.html")


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


if __name__ == "__main__":
    main_app.run()
