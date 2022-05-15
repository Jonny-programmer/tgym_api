from datetime import datetime
from app.data.db_session import create_session
from app.data.user import User
from app.data.posts import Post


class MemoryPostsRepo:
    def __init__(self):
        self.db_sess = create_session()

    def get_all(self):
        return tuple(self.db_sess.query(Post).all())

    def get_by_id(self, id):
        return tuple(self.db_sess.query(Post).filter(Post.id == id).first())

    def request_create(self, post, user_id):
        user = self.db_sess.query(User).filter(User.id == user_id).first()
        post.author = user
        post.created = datetime.now()
        self.db_sess.add(post)
        self.db_sess.commit()
        return post

    def request_delete(self, post_id, user):
        post = self.db_sess.query(Post).filter(Post.id == post_id).first()
        if not post:
            return f"Post does not exist for id {post_id}"
        if post.author.id != user.id:
            return f"You are not author of that post (id = {post_id})"
        post.delete()
        self.db_sess.commit()
        return None

    def get_by_username(self, username):
        user = self.db_sess.query(User).filter(User.username == username).first()
        posts = self.db_sess.query(Post).filter(Post.author == user).all()
        return tuple(posts)

    def get_by_category(self, category):
        posts = self.db_sess.query(Post).filter(Post.category == category).all()
        return tuple(posts)
