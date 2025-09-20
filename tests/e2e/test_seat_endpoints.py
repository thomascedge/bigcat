import json
from fastapi.testclient import TestClient
from uuid import uuid4
from src.seats.model import Seat, SeatResponse, SeatStatus, SeatType
from datetime import datetime

UID = str(uuid4())
seat = {
    'uid': UID,
    'concert_id': 'TESTCONCERT',
    'venue': 'TESTVENUE',
    'seat_number': 'TESTSEAT0',
    'seat_type': SeatType.REGULAR.value,
    'price': 100.00,
    'status': SeatStatus.AVAILABLE.value
}

seat_response = SeatResponse(seat_list=[Seat(**seat)])


def test_post(client: TestClient, auth_headers):
    # create seat
    create_response = client.post(
        '/seats/', 
        headers=auth_headers,
        json=seat_response.model_dump()
    )
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert seat['uid'] == create_response['seat_list'][0]['uid']
    assert seat['concert_id'] == create_response['seat_list'][0]['concert_id']
    assert seat['seat_number'] == create_response['seat_list'][0]['seat_number']
    assert seat['seat_type'] == create_response['seat_list'][0]['seat_type']
    assert seat['price'] == create_response['seat_list'][0]['price']
    assert seat['status'] == create_response['seat_list'][0]['status']

def test_get(client: TestClient, auth_headers):
    # get seat
    get_response = client.get(f'/seats/{seat['uid']}')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert seat['uid'] == get_response['uid']

    get_response = client.get('/seats/', params={'concert_id': seat['concert_id']})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert any(seat_response['uid'] == seat['uid'] for seat_response in get_response['seat_list'])

    get_response = client.get('/seats/', params={'venue': seat['venue']})
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert any(seat_response['venue'] == seat['venue'] for seat_response in get_response['seat_list'])

def test_put(client: TestClient, auth_headers):
    # edit seat
    update_seat = {
        'uid': UID,
        'concert_id': 'TESTCONCERT',
        'venue': 'TESTVENUE',
        'seat_number': 'TESTSEAT5',
        'seat_type': SeatType.REGULAR.value,
        'price': 100.00,
        'status': SeatStatus.AVAILABLE.value
    }

    update_response = client.put(f'/seats/edit/{seat['uid']}', 
                                 headers=auth_headers,
                                 json=update_seat)
    
    assert update_response.status_code == 200
    update_response = update_response.json()
    assert update_seat['seat_number'] == update_response['seat_number']

def test_delete(client: TestClient, auth_headers):
    # delete seat
    delete_response = client.delete(f'/seats/{seat['uid']}', headers=auth_headers)
    assert delete_response.status_code == 204

    # verify deletion
    get_deleted_response = client.get(f"/seats/{seat['uid']}", headers=auth_headers)
    assert get_deleted_response.status_code == 404


def test_seat_authorization(client: TestClient, auth_headers):
    # create seat
    seat = {
        'uid' : str(uuid4()),
        'concert_id' : 'TESTCONCERT',
        'venue' : 'TESTVENUE',
        'seat_number' : 'TESTSEAT0',
        'seat_type' : SeatType.REGULAR.value,
        'price' : 100.00,
        'status' : SeatStatus.AVAILABLE.value
    }

    seat_response = SeatResponse(seat_list=[Seat(**seat)])

    create_response = client.post(
        '/seats/',
        headers=auth_headers,
        json=seat_response.model_dump()
    )

    seat_id = create_response.json()

    # try accessing without auth
    endpoints = [
        ('POST', f'/seats/'),
        ('PUT', f'/seats/edit/{seat_id}'),
        ('DELETE', f'/seats/{seat_id}')
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401

def test_seat_not_found(client: TestClient, auth_headers):
    non_existent_id = ' '

    response = client.get(f'/seats/{non_existent_id}', params={'client_id': non_existent_id})
    assert response.status_code == 404

    seat_update = {
        'uid' : UID,
        'concert_id' : 'TESTCONCERT',
        'venue' : 'TESTVENUE',
        'seat_number' : 'TESTSEAT0',
        'seat_type' : SeatType.REGULAR.value,
        'price' : 100.00,
        'status' : SeatStatus.AVAILABLE.value
    } 

    response = client.put(f'/seats/edit/{non_existent_id}', headers=auth_headers, json=seat_update)
    assert response.status_code == 404

    response = client.delete(f'/seats/{non_existent_id}', headers=auth_headers)
    assert response.status_code == 204
