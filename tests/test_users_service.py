import pytest
from bson import ObjectId
from src.auth import service as auth_service
from src.users import service as users_service
from src.users.model import User, PasswordChange
from src.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError

def test_get_user_by_id(test_user, db):
    db['user'].insert_one(**test_user)

    user = users_service.get_user_by_id(test_user.id, db)
    assert user.id == test_user.id
    assert user.email == test_user.email

    with pytest.raises(UserNotFoundError):
        users_service.get_user_by_id(ObjectId(), db)

# def test_change_password(test_user, db):
