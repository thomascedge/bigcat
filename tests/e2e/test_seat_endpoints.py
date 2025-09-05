import json
from fastapi.testclient import TestClient
from uuid import uuid4
from src.seats.model import Seat, SeatResponse, SeatStatus, SeatType
from datetime import datetime
from src.logging import logger

def test_seat_crud_operations(client: TestClient, auth_headers):
    UID = str(uuid4())
    seat = Seat(
        uid=UID,
        concert_id='TESTCONCERT',
        seat_number='TESTSEAT0',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

    # create seat
    create_response = client.post(
        '/seats/', 
        headers=auth_headers,
        json={[seat.model_dump()]}
    )
    logger.debug(f'Create response: {create_response}')
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert seat.uid == create_response['uid']
    assert seat.concert_id == create_response['concert_id']
    assert seat.seat_number == create_response['seat_number']
    assert seat.seat_type == create_response['seat_type']
    assert seat.price == create_response['price']
    assert seat.status == create_response['status']

    # get seat
    get_response = client.get(f'/seats/{seat.uid}')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert seat.uid == get_response['uid']

    get_response = client.get('/seats/', params={'concert_id': seat.concert_id})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert seat.concert_id == any(seat_response['concert_id'] for seat_response in get_response['seat_list'])

    get_response = client.get('/seats/', params={'venue': seat.venue})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert seat.concert_id == any(seat_response['venue'] for seat_response in get_response['seat_list'])

    # edit seat
    update_seat = Seat(
        uid=UID,
        concert_id='TESTCONCERT',
        seat_number='TESTSEAT5',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

    update_response = client.put(f'/seats/edit/{seat.uid}', 
                                 headers=auth_headers,
                                 json={
                                     'seat_id': seat.uid,
                                     'seat_update': update_seat.model_dump()
                                     }
                                )
    assert update_response.status_code == 200
    update_response = update_response.json()
    assert update_seat.seat_number == update_response['seat_number']

    # delete seat
    delete_response = client.delete(f'/seats/{seat.uid}',
                  headers=auth_headers,
                  json={'seat_id': seat.uid}
                  )
    assert delete_response == 204

    # verify deletion
    get_deleted_response = client.get(f"/seats/{seat.uid}", headers=auth_headers)
    assert get_deleted_response.status_code == 404


def test_seat_authorization(client: TestClient):
    # create seat
    seat = Seat(
        uid=str(uuid4()),
        concert_id='TESTCONCERT',
        seat_number='TESTSEAT0',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

    create_response = client.post(
        '/seats/',
        json=seat.model_dump()
    )
    seat_id = create_response.uid

    # try accessing without auth
    endpoints = [
        ('POST', f'/seats/'),
        ('PUT', f'/seats/edit/{seat_id}'),
        ('DELETE', f'/seats/delete/{seat_id}')
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401

def test_seat_not_found(client: TestClient):
    non_existent_id = ' '

    response = client.get(f'/seats/', params={'client_id': non_existent_id})
    assert response.status_code == 404

    seat_update = Seat(
        uid=str(uuid4()),
        concert_id='TESTCONCERT',
        seat_number='TESTSEAT0',
        seat_type=SeatType.REGULAR.value,
        price=100.00,
        status=SeatStatus.AVAILABLE.value
    )

    response = client.put(f'/edit/{non_existent_id}', json=seat_update.model_dump())
    assert response.status_code == 404

    response = client.delete(f'/{non_existent_id}')
    assert response.status_code == 404
