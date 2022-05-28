from datetime import date

from flask.json import JSONEncoder
from sqlalchemy.orm import InstanceState

from app.data.posts import Post
from app.data.user import User


class MyJsonEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, date):
            return object.isoformat()
        elif isinstance(object, Post):
            res = object.__dict__
            del res['_sa_instance_state']
            return res
        elif isinstance(object, User):
            res = object.__dict__
            del res['_sa_instance_state']
            return res
        return super().default(object)