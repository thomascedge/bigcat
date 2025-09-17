import json
from fastapi.testclient import TestClient
from uuid import uuid4
from src.auth.service import get_password_hash
from src.bookings.model import Booking, BookingResponse, BookingStatus, PaymentStatus, BookingRequest, UpdateBookingRequest
from src.seats.model import Seat, SeatType, SeatStatus, SeatResponse
from src.concerts.model import ConcertStatus
from src.users.model import User
from datetime import datetime
from src.logging import logger

BOOKING_ID = str(uuid4())
USER_ID = str(uuid4())
CONFIRMATION_ID = str(uuid4())[:8]
CONCERT_ID = str(uuid4())
SEAT_ID = str(uuid4())
SEAT_ID_2 = str(uuid4())

booking = {
    'uid': BOOKING_ID,
    'user_id': USER_ID,
    'concert_id': CONCERT_ID,
    'venue': 'TESTVENUE',
    'seats': [SEAT_ID],
    'total_price': 100.00,
    'payment_status': PaymentStatus.SUCCESS.value,
    'status': BookingStatus.CONFIRMED.value,
    'request_datetime': str(datetime(2025, 1, 1)),
    'update_datetime': str(datetime(2025, 1, 1)),
    'confirmation_id': CONFIRMATION_ID
}

concert = {
    'uid': CONCERT_ID,
    'artist': 'TESTARTIST',
    'tour_name': 'TESTTOUR',
    'venue': 'TESTVENUE',
    'location': 'TESTLOCATION',
    'concert_datetime': str(datetime(2025, 1, 1).strftime("%Y-%m-%d %H:%M:%S")),
    'status': ConcertStatus.ON_SALE.value,
    'update_datetime': str(datetime.now())
}

seat = {
    'uid': SEAT_ID,
    'concert_id': CONCERT_ID,
    'venue': 'TESTVENUE',
    'seat_number': 'TESTSEAT0',
    'seat_type': SeatType.REGULAR.value,
    'price': 100.00,
    'status': SeatStatus.AVAILABLE.value
}

new_seat = {
    'uid': SEAT_ID_2,
    'concert_id': CONCERT_ID,
    'venue': 'TESTVENUE',
    'seat_number':' TESTSEAT1',
    'seat_type': SeatType.REGULAR.value,
    'price': 100.00,
    'status': SeatStatus.AVAILABLE.value
}

seat_response = SeatResponse(seat_list=[Seat(**seat)])

def test_crud(client: TestClient, auth_headers):
    _create_prereqs(client, auth_headers)

    # create booking
    payload = BookingRequest(
        concert_id=CONCERT_ID,
        seat_list=[SEAT_ID]
    )

    create_response = client.post(
        '/bookings/', 
        headers=auth_headers,
        json=payload.model_dump()
    )

    # get all bookings
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert create_response['concert_id'] == CONCERT_ID
    assert SEAT_ID in create_response['seats']
    
# def test_get(client: TestClient, auth_headers):
#     _create_prereqs(client, auth_headers)

    # # create booking
    # payload = BookingRequest(
    #     concert_id=CONCERT_ID,
    #     seat_list=[SEAT_ID]
    # )

    # create_response = client.post(
    #     '/bookings/', 
    #     headers=auth_headers,
    #     json=payload.model_dump()
    # )

    # create_response = create_response.json()
    booking_id = create_response['uid']

    # search bookings
    get_response = client.get('/bookings/search', headers=auth_headers, params={'booking_id': booking_id})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert any(booking['uid'] for booking in get_response['booking_list'])

    get_response = client.get('/bookings/search', headers=auth_headers, params={'venue': 'TESTVENUE'})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert any(booking['uid'] for booking in get_response['booking_list'])

# def test_patch(client: TestClient, auth_headers):
#     _create_prereqs(client, auth_headers)

    # payload = BookingRequest(
    #     concert_id=CONCERT_ID,
    #     seat_list=[SEAT_ID]
    # )
    
    # create_response = client.post(
    #     '/bookings/', 
    #     headers=auth_headers,
    #     json=payload.model_dump()
    # )

    # create_response = create_response.json()
    # booking_id = create_response['uid']

    # add seat to bookng
    patch_response = client.patch(
        f'/bookings/{booking_id}/add/{SEAT_ID_2}',
        headers=auth_headers
    )
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert SEAT_ID_2 in patch_response['seats']

    # remove seat from booking
    patch_response = client.patch(
        f'/bookings/{booking_id}/remove/{SEAT_ID_2}',
        headers=auth_headers
    )
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert SEAT_ID_2 not in patch_response['seats']

    # cancel booking
    patch_response = client.patch(f'/bookings/{booking_id}/cancel', headers=auth_headers)
    assert patch_response.status_code == 200
    patch_response = patch_response.json()
    assert patch_response['status'] == BookingStatus.CANCELED.value

# def test_put(client: TestClient, auth_headers):
#     _create_prereqs(client, auth_headers)

    # payload = BookingRequest(
    #     concert_id=CONCERT_ID,
    #     seat_list=[SEAT_ID]
    # )
    
    # create_response = client.post(
    #     '/bookings/', 
    #     headers=auth_headers,
    #     json=payload.model_dump()
    # )

    # create_response = create_response.json()
    # booking_id = create_response['uid']

    # edit booking
    booking_update = {
        'uid': booking_id,
        'user_id': USER_ID,
        'concert_id': CONCERT_ID,
        'venue': 'TESTVENUE',
        'seats': [SEAT_ID, SEAT_ID_2],
        'total_price': 100.00,
        'payment_status': PaymentStatus.FAILED.value,
        'status': BookingStatus.CANCELED.value,
        'request_datetime': str(datetime(2025, 1, 1)),
        'update_datetime': str(datetime(2025, 1, 1)),
        'confirmation_id': CONFIRMATION_ID
    }

    payload = UpdateBookingRequest(
        booking_id=booking_id,
        booking_update=booking_update
    )

    update_response = client.put(
        f'/bookings/', 
        headers=auth_headers,
        json=payload.model_dump()
    )

    assert update_response.status_code == 200
    update_response = update_response.json()
    assert booking_update['payment_status'] == update_response['payment_status']
    assert booking_update['status'] == update_response['status']

def test_booking_authorization(client: TestClient, auth_headers):
    _create_prereqs(client, auth_headers)

    booking_id = booking['uid']

    payload = BookingRequest(
        concert_id=CONCERT_ID,
        seat_list=[SEAT_ID]
    )

    create_booking = client.post(
        '/bookings/',
        headers=auth_headers,
        json=payload.model_dump()
    )

    # try accessing without auth
    endpoints = [
        ('GET', f'/bookings/'),
        ('GET', f'/bookings/search'),
        ('POST', f'/bookings/'),
        ('PATCH', f'/bookings/{booking_id}/add/{SEAT_ID}'),
        ('PATCH', f'/bookings/{booking_id}/remove/{SEAT_ID}'),
        ('PATCH', f'/bookings/{booking_id}/cancel'),
        ('PUT', f'/bookings/')
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401

def test_booking_not_found(client: TestClient, auth_headers):
    non_existent_id = ' '

    response = client.get(f'/bookings/search', headers=auth_headers, params={'booking_id': non_existent_id})
    assert response.status_code == 404

    USER_ID = str(uuid4())

    current_user = {
        'uid': USER_ID,
        'first_name': 'Test',
        'last_name': 'User',
        'email':' test@example.com',
        'password_hash': get_password_hash('password123'),
        'admin': False
    }

    seat_update = {
        'uid': str(uuid4()),
        'concert_id': 'TESTCONCERT',
        'seat_number':' TESTSEAT0',
        'venue':' TESTVENUE',
        'seat_type': SeatType.REGULAR.value,
        'price': 100.00,
        'status': SeatStatus.AVAILABLE.value
    }

    booking_update = {
        'uid': str(uuid4()),
        'user_id': USER_ID,
        'concert_id': 'TESTCONCERT',
        'venue': 'TESTVENUE',
        'seats': ['TESTSEAT0', 'TESTSEAT1'],
        'total_price': 100.00,
        'payment_status': PaymentStatus.FAILED.value,
        'status': BookingStatus.CANCELED.value,
        'request_datetime': str(datetime(2025, 1, 1)),
        'update_datetime': str(datetime(2025, 1, 1)),
        'confirmation_id': str(uuid4())[:8]
    }

    response = client.patch(f'/bookings/{non_existent_id}/add/{SEAT_ID_2}', headers=auth_headers)
    assert response.status_code == 404

    response = client.patch(f'/bookings/{non_existent_id}/remove/{SEAT_ID_2}', headers=auth_headers)
    assert response.status_code == 404

    response = client.patch(f'/bookings/{non_existent_id}/cancel', headers=auth_headers)
    assert response.status_code == 404

    payload = UpdateBookingRequest(
        booking_id=non_existent_id,
        booking_update=booking_update
    )

    response = client.put(
        f'/bookings',
        headers=auth_headers, 
        json=payload.model_dump()
    )
    assert response.status_code == 404

def _create_prereqs(client, auth_headers):
    # create seat
    client.post(
        '/seats/', 
        headers=auth_headers,
        json=seat_response.model_dump()
    )

    # create concert
    client.post(
        '/concerts/',
        headers=auth_headers,
        json=concert
    )