from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from app.data.db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean)
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Пользователь, который создал этот пост
    author = orm.relation('User')
