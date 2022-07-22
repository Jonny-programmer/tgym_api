from datetime import datetime

from app.data.user import User
from app.data.db_session import create_session


class MemoryUsersRepo:
    def __init__(self):
        self.db_sess = create_session()

    def get_all(self):
        return self.db_sess.query(User).all()

    def get_by_id(self, id):
        user = self.db_sess.query(User).filter(User.id == id).first()
        return user

    def get_by_name(self, username):
        user = self.db_sess.query(User).filter(User.username == username).first()
        print("got user by name:", user)
        return user

    def request_create(self, username, name, surname, email, password):
        user = self.get_by_name(username)
        if user:
            return None  # Пользователь с таким именем уже есть
        new_user = User(
            username=username,
            name=name,
            surname=surname,
            email=email,
            created_date=datetime.now()
        )
        new_user.set_password(password)
        self.db_sess.add(new_user)
        self.db_sess.commit()
        return new_user

    def request_update(self, id, username, name, surname, email, password):
        user = self.db_sess.query(User).get(id)
        user.username = username
        user.name = name
        user.surname = surname
        user.email = email
        user.set_password(password)
        self.db_sess.add(user)
        self.db_sess.commit()

    def request_delete(self, id):
        self.db_sess.query(User).get(id).delete()
        self.db_sess.commit()

    def authorize(self, login, password):
        user = self.get_by_name(login)
        if not user:
            return None, "No such user"
        if not user.check_password(password):
            return None, "Wrong password"
        return user, ""