import jwt, os, bcrypt
from datetime import datetime, timedelta, timezone
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import HTTPException
from jwt import InvalidTokenError

from app.models.users import User
from app.db.users_repo import fetch_user


dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCES_TOKEN_EXPIRE_MINUTES", 60))


def login(username: str | None, email: str | None, password: str) -> User:
    if username is None and email is None:
        raise ValueError("Must provide username or email")

    if username and email:
        raise ValueError("Can only provide either username or email")

    user = fetch_user(username=username, email=email)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not bcrypt.checkpw(
        password.encode("utf-8"), user["hashed_password"].encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return User.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_user(username: str | None, email: str | None, password: str) -> dict:
    user = login(username, email, password)
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
