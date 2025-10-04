import jwt, os, bcrypt
from datetime import datetime, timedelta, timezone
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from typing import Annotated

from app.models.users import User, Token, TokenData
from app.db.users_repo import fetch_user, get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def login(username: str | None, email: str | None, password: str) -> User:
    if username is None and email is None:
        raise ValueError("Must provide username or email")

    if username and email:
        raise ValueError("Can only provide either username or email")

    user, user_in_db = fetch_user(username=username, email=email)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not bcrypt.checkpw(
        password.encode("utf-8"), user_in_db.hashed_password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return User.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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


def login_for_access_token(
    username: str | None, email: str | None, password: str
) -> dict:
    user = login(username, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user
