from waitress import serve

from api.posts import PostListRes, PostRes
from api.users import RegisterRes, LoginRes, UserPosts
from app.app import main_app


@main_app.route('/', defaults={'path': ''})
@main_app.route('/u/<path:path>')
@main_app.route('/a/<path:path>')
def root(path):
    return main_app.send_static_file("index.html")


main_app.api.add_resource(RegisterRes, "/api/register")
main_app.api.add_resource(LoginRes, "/api/login")
main_app.api.add_resource(PostListRes, "/api/posts/<category_name>", "/api/posts/")
main_app.api.add_resource(PostRes, "/api/post/<int:post_id>")
main_app.api.add_resource(UserPosts, "/api/user/<user_login>")


if __name__ == "__main__":
    # main_app.run()
    serve(main_app)
