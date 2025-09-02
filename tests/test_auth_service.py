import pytest
from datetime import timedelta
from bson.objectid import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import service as auth_service
from src.auth.model import RegisterUserRequest
from src.exceptions import AuthenticationError
from src.users.model import User

class TestAuthService():
    def test_verify_password(self):
        password = 'password123'
        hashed = auth_service.get_password_hash(password)
        assert auth_service.verify_password(password, hashed)
        assert not auth_service.verify_password('wrongpassword', hashed)

    def test_authenticate_user(self, test_user, db):
        db['user'].add(test_user)

        user = auth_service.authenticate_user('test@example.com', 'password123', db)
        assert user is not False
        assert user.email == test_user.email

        class FormData:
            def __init__(self):
                self.username = 'test@example'
                self.password = 'password123'
                self.scope = ''
                self.client_id = None
                self.client_secret = None

        form_data = FormData()
        token = auth_service.login_for_access_token(form_data, db)
        assert token.token_type == 'bearer'
        assert token.access_token is not None


@pytest.mark.asyncio
async def test_register_user(db):
    request = RegisterUserRequest(
        email='new@example.com',
        password='password123',
        first_name='New',
        last_name='User'
    )
    auth_service.register_user(db, request)

    user = db['user'].find_one({'email': 'new@example.com'})
    assert user is not None
    assert user.email == 'new@example.com'
    assert user.password == 'password123'
    assert user.first_name == 'New'
    assert user.last_name =='User'

def test_create_and_verify_token(db):
    user_id = ObjectId()
    token = auth_service.create_access_token('test@example.con', user_id, timedelta(minutes=30))

    token_data = auth_service.verify_token(token)
    assert token_data.get_userid() == user_id

    # test invalid credentials
    assert auth_service.authenticate_user('test@example.com', 'wrongpassword', db) is False

    with pytest.raises(AuthenticationError):
        form_data = OAuth2PasswordRequestForm(
            username='test@example.com',
            password='wrongpassword',
            scope=''
        )
        auth_service.login_for_access_token(form_data, db)