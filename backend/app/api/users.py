from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_admin
from app.schemas.user import UserOut
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: DbSession):
    return user_service.list_users(db)