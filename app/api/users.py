from fastapi import APIRouter, HTTPException

from app.models.users import UserCreate, User, LoginRequest, Token
from app.db.users_repo import create_user
from app.services.users import login_for_access_token

router = APIRouter()


@router.post("/users", response_model=User, tags=["auth"])
def register_user(user_data: UserCreate):
    try:
        user = create_user(user_data.username, user_data.email, user_data.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token, tags=["auth"])
def login(login_request: LoginRequest):
    return login_for_access_token(**login_request.model_dump())
