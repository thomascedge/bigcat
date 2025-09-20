import pytest
from datetime import datetime, timezone
from uuid import uuid4
from database.core import client as db_client
from auth.model import TokenData
from auth.service import get_password_hash
from rate_limiting import limiter
from users.model import User
from concerts.model import Concert, ConcertStatus
from bookings.model import Booking, BookingStatus, PaymentStatus
from seats.model import Seat, SeatType, SeatStatus

USER_ID = str(uuid4())
CONFIRMATION_ID = str(uuid4())[:8]
CONCERT_ID = str(uuid4())

@pytest.fixture(scope='function')
def db_session():
    assert db_client.admin.command("ping")["ok"] != 0.0
    return db_client['bigcat']

    # try:
    #     yield db_client
    # finally:
    #     db_client.close()

@pytest.fixture(scope='function')
def test_user():
    # Create a user with a known password hash
    return User(
        uid=USER_ID,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        password_hash=get_password_hash('password123'),
        admin=False
    )

@pytest.fixture(scope='function')
def test_user_admin():
    # Create a user with a known password hash
    return User(
        uid=USER_ID,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        password_hash=get_password_hash('password123'),
        admin=True
    )

@pytest.fixture(scope='function')
def test_token_data():
    return TokenData(uid=str(uuid4()))

@pytest.fixture(scope='function')
def client(db_session):
    from main import app
    from database.core import get_database

    # diable rate limiting for tests
    limiter.reset()

    def override_get_db():
        return db_session
        # try:
        #     yield db_session
        # finally:
        #     db_session.close()

    app.dependency_overrides[get_database] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope='function')
def auth_headers(client, db_session):
    # register a test user
    response = client.post(
        '/auth/',
        json={
            'email': 'admin@example.com',
            'password': 'testpassword123',
            'first_name': 'Admin',
            'last_name': 'User',
            'admin': True
        }
    )
    assert response.status_code == 201

    # login to get access token
    response = client.post(
        '/auth/token',
        data={
            "username": "admin@example.com",
            "password": "testpassword123",
            "grant_type": "password"
        }
    )
    assert response.status_code == 200
    token = response.json()['access_token']

    return {'Authorization': f'Bearer {token}'}

@pytest.fixture(scope='function')
def test_concert(test_token_data):
    return Concert(
        uid=CONCERT_ID,
        artist='TESTARTIST',
        tour_name='TESTTOUR',
        venue='TESTVENUE',
        location='TESTLOCATION',
        concert_datetime=datetime(2025, 1, 1),
        status=ConcertStatus.ON_SALE.value,
        update_datetime=datetime.now()
    )

@pytest.fixture(scope='function')
def test_booking(test_token_data):
    return Booking(
        uid=str(uuid4()),
        user_id=USER_ID,
        concert_id=CONCERT_ID,
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.SUCCESS,
        status=BookingStatus.CONFIRMED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=CONFIRMATION_ID
    )

@pytest.fixture(scope='function')
def test_booking_2(test_token_data):
    return Booking(
        uid=str(uuid4()),
        user_id=USER_ID,
        concert_id=CONCERT_ID,
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.FAILED,
        status=BookingStatus.CANCELED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=CONFIRMATION_ID
    )

@pytest.fixture(scope='function')
def test_seat(test_token_data):
    return Seat(
        uid=str(uuid4()),
        concert_id=CONCERT_ID,
        venue='TESTVENUE',
        seat_number='TESTSEAT0',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

@pytest.fixture(scope='function')
def test_seat_2(test_token_data):
    return Seat(
        uid=str(uuid4()),
        concert_id='TESTCONCERT',
        venue='TESTVENUE',
        seat_number='TESTSEAT5',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )
