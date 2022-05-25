from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from app.data.db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Пользователь, который создал этот пост
    author = orm.relation('User')

    def __getattr__(self, item):
        print(item)
        return self.__getattribute__(item)
