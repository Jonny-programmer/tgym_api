from datetime import date

from flask.json import JSONEncoder

from app.data.posts import Post
from app.data.user import User


class MyJsonEncoder(JSONEncoder):
    def default(self, object):
        print("\n\n")
        print("---------->", "Well, we are into")
        if isinstance(object, date):
            return object.isoformat()
        elif isinstance(object, Post):
            print("And it works!")
            print(object.__dict__)
            print("\n\n")
            return object.__dict__
        elif isinstance(object, User):
            return object.__dict__
        return super().default(object)