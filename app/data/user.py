import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now, autoincrement=True)
    # Все публикации пользователя
    posts = orm.relation('Post', back_populates='author')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __getattr__(self, item):
        if self.item:
            return self.item
        return None