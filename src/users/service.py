from fastapi import HTTPException, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from src.users.model import *
from src.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from src.auth.service import verify_password, get_password_hash
from src.logging import logger
from src.database.core import get_database


def get_user_by_id(user_id: str, db: Database=Depends(get_database)) -> User:
    user = db['user'].find_one({'uid': user_id})
    if not user:
        logger.warning(f'User not found with uid: {user_id}')
        raise UserNotFoundError(user_id)
    logger.info(f'Successfully retrieved user with uid: {user_id}')
    return User(**user)

def change_password(user_id: str, password_change: PasswordChange, db: Database=Depends(get_database)) -> None:
    try:
        user = get_user_by_id(user_id, db)

        # verify current password
        if not verify_password(password_change.current_password, user.password_hash):
            logger.warning(f'Invalid current password provided for user: {user_id}')
            raise InvalidPasswordError()
        
        # verify new passwords match
        if password_change.new_password != password_change.new_password_confirm:
            logger.warning(f'Password mismatch during change attempt for user: {user_id}')
            raise PasswordMismatchError()

        # update password
        user.password_hash = get_password_hash(password_change.new_password)
        db['user'].update_one({'uid': str(user.uid)}, {'$set': {'password_hash' : user.password_hash}})

        logger.info(f'Succesfully changed password for user: {user_id}')

    except Exception as e:
        logger.error(f'Error durring password change for user {user_id}. Error {str(e)}')
        raise
