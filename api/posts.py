from flask import jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, abort
from app.app import main_app
from resources.users_repo import User
from resources.posts_repo import Post


parser = reqparse.RequestParser()
parser.add_argument('category', required=True)
parser.add_argument('type', required=True)
parser.add_argument('title', required=True)
parser.add_argument('text', required=False)
parser.add_argument('url', required=False)


class PostRes(Resource):
    def get(self, post_id):
        return jsonify(main_app.posts_repo.get_by_id(post_id))

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
        return jsonify(main_app.posts_repo.get_all())

    @jwt_required
    def post(self):
        args = parser.parse_args()
        post = Post(**dict(args))
        post.author = User(**get_jwt_identity())
        post = main_app.posts_repo.request_create(post)
        return jsonify(post)
