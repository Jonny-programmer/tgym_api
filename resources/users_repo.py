from tools.get_cursor import get_connection_cursor
from tools.my_dict import MyDict


class User(MyDict):
    pass


class SqliteUsersRepo:
    def __init__(self, name):
        self.name = name

    def get_all(self):
        query = """SELECT id, username, password FROM users"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query).fetchall()
        res = list()
        for elem in results:
            res.append(User(id=elem[0], username=elem[1], password=elem[2]))
        con.close()
        return res

    def get_by_id(self, id):
        query = """SELECT id, username, password FROM users WHERE id=?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (id,)).fetchone()
        con.close()
        if not result:
            return None
        return User(id=result[0], username=result[1], password=result[2])

    def get_by_name(self, username):
        query = """SELECT id, username, password FROM users WHERE username=?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (username,)).fetchone()
        con.close()
        if not result:
            return None
        return User(id=result[0], username=result[1], password=result[2])

    def request_create(self, username, password):
        user = self.get_by_name(username)
        if not (user is None):
            return None  # Пользователь с таким именем уже есть
        query = """INSERT INTO users(username, password) VALUES (?, ?)"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (username, password))
        if not result.rowcount > 0:
            con.close()
            return None
        new_user = User(id=result.lastrowid, username=username, password=password)
        con.commit()
        con.close()
        return new_user

    def request_update(self, id, username, password):
        query = """UPDATE users SET username=?, password=? WHERE id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (username, password, id))
        con.commit()
        con.close()

    def request_delete(self, id):
        query = """DELETE FROM users WHERE id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (id,))
        con.commit()
        con.close()

    def authorize(self, login, password):
        user = self.get_by_name(login)
        if not user:
            return None, "No such user"
        if user.password != password:
            return None, "Wrong password"
        return user, ""