from auth.oauth import pwd_context
from db.connection import db_con, db_cursor
from typing import List
from auth.user import User
from typing import Union


def user_tuple_factory(u):
    return User(**{
        "id": u[0],
        "username": u[1],
        "password": u[2],
        "admin": u[3] == 1
    })


def create_users_table():
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        admin INTEGER NOT NULL
    )""")

    db_cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, admin) VALUES (?, ?, ?)",
        ("admin", pwd_context.hash("admin"), 1)
    )


def create_new_user(username: str, password: str, admin: bool = False):
    db_cursor.execute(
        "INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
        (username, pwd_context.hash(password), 1 if admin else 0)
    )
    db_con.commit()


def get_all_users() -> List[User]:
    return [user_tuple_factory(u) for u in db_cursor.execute("SELECT * FROM users").fetchall()]


def get_user_by_username(username: str) -> Union[User, None]:
    res = db_cursor.execute("SELECT * FROM users WHERE username=?", [username]).fetchone()
    return None if res is None else user_tuple_factory(res)


def update_user_password(user_id: int, password: str):
    db_cursor.execute("UPDATE users SET password=? WHERE id=?", (pwd_context.hash(password), user_id))
    db_con.commit()