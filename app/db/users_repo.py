from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
import bcrypt

from .connection import get_connection
from app.models.users import User


def create_user(username: str, email: str, password: str) -> User:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            """SELECT *
            FROM users
            WHERE username=%s
            OR email=%s 
            ;
            """,
            (username, email),
        )
        if cur.fetchone():
            raise ValueError("An account with this username or email already exists")
        else:
            cur.execute(
                """
                INSERT INTO users (username, email, hashed_password)
                VALUES (%s, %s, %s)
                RETURNING *
                ;
                """,
                (username, email, hashed_password.decode("utf-8")),
            )
            user = cur.fetchone()
            conn.commit()

        return User(id=user["id"], username=user["username"], email=user["email"])


def fetch_user(username: str | None, email: str | None) -> User:
    if username is None and email is None:
        raise ValueError("Must provide username or email")
    if username and email:
        raise ValueError("Can only provide either username or email")
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT *
            FROM users
            WHERE username=%s
            OR email=%s
            ;
            """,
            (username, email),
        )
        user = cur.fetchone()
        return User(id=user["id"], username=user["username"], email=user["email"])
