from fastapi import APIRouter, Depends, status
from pymongo.database import Database
from app.users import model
from app.users import service
from app.database.core import DbSession
from app.auth.service import CurrentUser

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/me', response_model=model.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(current_user.uid, db)

@router.put('/change-password', status_code=status.HTTP_200_OK)
def change_password(password_change: model.PasswordChange, current_user: CurrentUser, db: DbSession):
    service.change_password(current_user.uid, password_change, db)
    