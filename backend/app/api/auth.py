from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, DbSession
from app.schemas.user import Token, UserOut, UserRegister
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: DbSession):
    try:
        return auth_service.register_user(db, data)
    except auth_service.EmailAlreadyExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Пользователь с таким email уже существует")


@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    try:
        token = auth_service.authenticate(db, form.username, form.password)
    except auth_service.InvalidCredentials:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user