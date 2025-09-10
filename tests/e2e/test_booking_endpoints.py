import json
from fastapi.testclient import TestClient
from uuid import uuid4
from src.auth.service import get_password_hash
from src.bookings.model import Booking, BookingResponse, BookingStatus, PaymentStatus
from src.seats.model import Seat, SeatType, SeatStatus
from src.users.model import User
from datetime import datetime
from src.logging import logger

def test_booking_crud_operations(client: TestClient, auth_headers):
    USER_ID = str(uuid4())
    CONFIRMATION_ID = str(uuid4())[:8]

    booking = Booking(
        uid=str(uuid4()),
        user_id=USER_ID,
        concert_id='TESTCONCERT',
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.SUCCESS,
        status=BookingStatus.CONFIRMED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=CONFIRMATION_ID
    )

    # create booking
    client.post(
        '/bookings/', 
        headers=auth_headers,
        json=json.dumps(booking.model_dump(), indent=4, sort_keys=True, default=str)
    )

    # get all bookings
    create_response = client.get('/bookings/', headers=auth_headers)
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert booking.uid == create_response['uid']
    assert booking.user_id == create_response['user_id']
    assert booking.venue == create_response['venue']
    assert booking.seats == create_response['seats']
    assert booking.total_price == create_response['total_price']
    assert booking.payment_status == create_response['payment_status']
    assert booking.status == create_response['status']
    assert booking.request_datetime == create_response['request_datetime']
    assert booking.confirmation_id == create_response['confirmation_id']

    # search bookings
    get_response = client.get('/bookings/search', headers=auth_headers, params={'booking_id': booking.uid})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert booking.uid == get_response['uid']

    get_response = client.get('/bookings/search', headers=auth_headers, params={'venue': 'TESTVENUE'})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert booking.uid == get_response['uid']

    # add seat to bookng
    patch_response = client.patch(
        f'/bookings/{booking.uid}/add',
        headers=auth_headers, 
        json={
            'booking_id': booking.uid,
            'seat_id': 'TESTSEAT5'
        }
    )
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert 'TESTSEAT5' in patch_response['seats']


    # remove seat from booking
    patch_response = client.patch(
        f'/bookings/{booking.uid}/remove',
        headers=auth_headers,
        json={
            'booking_id': booking.uid,
            'seat_id': 'TESTSEAT5'
        }
    )
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert 'TESTSEAT5' not in patch_response['seats']

    # cancel booking
    patch_response = client.patch(f'/bookings/{booking.uid}/add', headers=auth_headers)
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert patch_response['status'] == BookingStatus.CANCELED.value

    # edit booking
    booking_update = Booking(
        uid=str(uuid4()),
        user_id=USER_ID,
        concert_id='TESTCONCERT',
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.FAILED,
        status=BookingStatus.CANCELED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=CONFIRMATION_ID
    )

    update_response = client.put(
        f'/bookings/', 
        headers=auth_headers,
        json={
            "booking_id": booking.uid,
            "booking_update": json.dumps(booking_update.model_dump(), indent=4, sort_keys=True, default=str)
        }
    )
    assert update_response.status_code == 200
    update_response = update_response.json()
    assert booking_update.payment_status == update_response['payment_status']
    assert booking_update.status == update_response['status']

def test_booking_authorization(client: TestClient):
    # create booking
    booking = Booking(
        uid=str(uuid4()),
        user_id=str(uuid4()),
        concert_id='TESTCONCERT',
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.SUCCESS,
        status=BookingStatus.CONFIRMED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=str(uuid4())[:8]
    )

    booking_id = booking.uid

    # try accessing without auth
    endpoints = [
        ('GET', f'/bookings/'),
        ('GET', f'/bookings/searc'),
        ('POST', f'/bookings/'),
        ('PATCH', f'/bookings/{booking_id}/add'),
        ('PATCH', f'/bookings/{booking_id}/remove'),
        ('PATCH', f'/bookings/{booking_id}/cancel'),
        ('PUT', f'/bookings/')
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401

def test_booking_not_found(client: TestClient):
    non_existent_id = ' '

    response = client.get(f'/bookings/search', params={'booking_id': non_existent_id})
    assert response.status_code == 404

    USER_ID = str(uuid4())

    current_user = User(
        uid=USER_ID,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        password_hash=get_password_hash('password123')
    )

    seat_update = Seat(
        uid=str(uuid4()),
        concert_id='TESTCONCERT',
        seat_number='TESTSEAT0',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

    booking_update = Booking(
        uid=str(uuid4()),
        user_id=USER_ID,
        concert_id='TESTCONCERT',
        venue='TESTVENUE',
        seats=['TESTSEAT0', 'TESTSEAT1'],
        total_price=100.00,
        payment_status=PaymentStatus.FAILED,
        status=BookingStatus.CANCELED.value,
        request_datetime=datetime(2025, 1, 1),
        update_datetime=datetime(2025, 1, 1),
        confirmation_id=str(uuid4())[:8]
    )

    response = client.patch(f'/bookings/{non_existent_id}/add', 
                            json={
                                'current_user': current_user.model_dump(),
                                'booking_id': non_existent_id,
                                'seat_id': seat_update.uid
                                })
    assert response.status_code == 404

    response = client.patch(f'/bookings/{non_existent_id}/remove', 
                            json={
                                'current_user': current_user.model_dump(),
                                'booking_id': non_existent_id,
                                'seat_id': seat_update.uid
                                })
    assert response.status_code == 404

    response = client.patch(f'/bookings/{non_existent_id}/cancel', 
                            json={
                                'current_user': current_user.model_dump(),
                                'booking_id': non_existent_id
                                })
    assert response.status_code == 404

    response = client.put(f'/bookings', 
                            json={
                                'current_user': current_user.model_dump(),
                                'booking_id': non_existent_id,
                                'booking_update': booking_update
                                })
    assert response.status_code == 404
