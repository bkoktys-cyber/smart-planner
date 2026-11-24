from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas.user import UserRegister


class EmailAlreadyExists(Exception):
    pass


class InvalidCredentials(Exception):
    pass


def register_user(db: Session, data: UserRegister) -> User:
    if db.scalar(select(User).where(User.email == data.email)):
        raise EmailAlreadyExists()
    user = User(
        email=data.email,
        name=data.name,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> str:
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentials()
    return create_access_token(user.id, user.role)