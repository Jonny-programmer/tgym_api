from datetime import datetime
from resources.users_repo import User
from tools.my_dict import MyDict


class Post(MyDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = []
        self.comments = []
        self.upvotePercentage = 100
        if self.author:
            self.author = User(**self.author)


class InMemoryPostsRepo:
    def __init__(self):
        self.next_id = 1
        self.by_id = {}

    def get_all(self):
        return tuple(self.by_id.values())

    def get_by_id(self, id):
        return self.by_id.get(id, None)

    def request_create(self, post):
        post.id = self.next_id
        post.created = datetime.now()
        self.by_id[post.id] = post
        self.next_id += 1
        return post

    def request_delete(self, post_id, user):
        p = self.get_by_id(post_id)
        if not p:
            return f"Post does not exist for id {post_id}"
        if p.author.id != user.id:
            return f"You are not author of that post (id = {post_id})"
        del self.by_id[post_id]
        return None

    def get_by_username(self, username):
        result = []
        for _, post in self.by_id.items():
            if post.author.username == username:
                result.append(post)
        return tuple(result)

    def get_by_category(self, category):
        result = []
        for _, post in self.by_id.items():
            if post.category == category:
                result.append(post)
        return tuple(result)