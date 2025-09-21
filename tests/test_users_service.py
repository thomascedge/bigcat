import pytest
from uuid import uuid4
from app.auth import service as auth_service
from app.users import service as users_service
from app.users.model import User, PasswordChange
from app.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError

def test_get_user_by_id(test_user, db_session):
    db_session['user'].insert_one(test_user.model_dump())

    user = users_service.get_user_by_id(test_user.uid, db_session)
    assert user.uid == test_user.uid
    assert user.email == test_user.email

    with pytest.raises(UserNotFoundError):
        users_service.get_user_by_id(str(uuid4()), db_session)

def test_change_password(test_user, db_session):
    # add the user to the database
    db_session['user'].insert_one(test_user.model_dump())

    # test successful password chage
    password_change = PasswordChange(
        current_password='password123',
        new_password='newpassword123',
        new_password_confirm='newpassword123'
    )

    users_service.change_password(test_user.uid, password_change, db_session)

    # verify new password works
    updated_user = db_session['user'].find_one({'uid': test_user.uid})
    updated_user = User(**updated_user)
    assert auth_service.verify_password('newpassword123', updated_user.password_hash)

def test_change_password_invalid_current(test_user, db_session):
    db_session['user'].insert_one(test_user.model_dump())

    # test invalid current password
    with pytest.raises(InvalidPasswordError):
        password_change = PasswordChange(
            current_password='wrongpassword',
            new_password='newpassword123',
            new_password_confirm='newpassword123'
        )

        users_service.change_password(test_user.uid, password_change, db_session)

def test_change_password_mismatch(test_user, db_session):
    db_session['user'].insert_one(test_user.model_dump())

    # test invalid current password
    with pytest.raises(InvalidPasswordError):
        password_change = PasswordChange(
            current_password='password123',
            new_password='newpassword123',
            new_password_confirm='differentpassword'
        )

        users_service.change_password(test_user.uid, password_change, db_session)
