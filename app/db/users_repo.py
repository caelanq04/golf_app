from uuid import UUID
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
import bcrypt
from typing import Optional, Tuple

from .connection import get_connection
from app.models.users import User, UserInDB


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


def get_user_by_id(user_id: UUID) -> str:
    if user_id is None:
        return None
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id =%s;", (str(user_id),))
        result = cur.fetchone()
        return result[0] if result else None


def fetch_user(
    username: str | None, email: str | None
) -> Tuple[Optional[User], Optional[UserInDB]]:
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
        if not user:
            return None, None

        return User(
            id=user["id"], username=user["username"], email=user["email"]
        ), UserInDB(hashed_password=user["hashed_password"])
