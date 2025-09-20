import json
from fastapi.testclient import TestClient
from uuid import uuid4
from src.concerts.model import Concert, ConcertStatus, ConcertResponse
from datetime import datetime

concert_id = str(uuid4())

concert = {
    'uid': concert_id,
    'artist': 'TESTARTIST',
    'tour_name': 'TESTTOUR',
    'venue': 'TESTVENUE',
    'location': 'TESTLOCATION',
    'concert_datetime': str(datetime(2025, 1, 1).strftime("%Y-%m-%d %H:%M:%S")),
    'status': ConcertStatus.ON_SALE.value,
    'update_datetime': str(datetime.now())
}

concert_update = {
    'uid': concert_id,
    'artist': 'TESTARTIST1',
    'tour_name': 'TESTTOUR1',
    'venue': 'TESTVENUE1',
    'location': 'TESTLOCATION1',
    'concert_datetime': str(datetime(2025, 1, 1).strftime("%Y-%m-%d %H:%M:%S")),
    'status': ConcertStatus.COMPLETED.value,
    'update_datetime': str(datetime.now())
}


def test_post(client: TestClient, auth_headers):    
    # create concert
    create_response = client.post(
        '/concerts/',
        headers=auth_headers,
        json=concert
    )
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert concert['uid'] == create_response['uid']
    assert concert['artist'] == create_response['artist']
    assert concert['tour_name'] == create_response['tour_name']
    assert concert['venue'] == create_response['venue']
    assert concert['location'] == create_response['location']
    # assert concert['datetime'] == create_response['datetime']
    assert concert['status'] == create_response['status']

def test_get(client: TestClient):
    # get concert
    get_response = client.get(f'/concerts/id/{concert['uid']}')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert concert['uid'] == get_response['uid']

    # get all concerts
    get_response = client.get(f'/concerts/')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert len(get_response) > 0
    assert any(concert['uid'] == returned_concert['uid'] for returned_concert in get_response['concert_list'])

    # search concert
    params = { 
        'artist': 'TESTARTIST',
        'tour_name': 'TESTTOUR',
        'venue': 'TESTVENUE',
        'location': 'TESTLOCATION',
        'concert_datetime': datetime(2025, 1, 1)
    }

    search_response = client.get(
        f'/concerts/search/',
        params=params
    )
    assert search_response.status_code == 200
    search_response = search_response.json()
    assert any(concert['uid'] == returned_concert['uid'] for returned_concert in search_response['concert_list'])

    # search concert by concert id
    search_response = client.get(
        f'/concerts/search/',
        params={ 
            'concert_id': concert['uid']
        }
    )
    assert search_response.status_code == 200
    search_response = search_response.json()
    assert any(concert['uid'] == returned_concert['uid'] for returned_concert in search_response['concert_list'])

def test_patch(client: TestClient, auth_headers):
    # update concert
    update_response = client.patch(
        f'/concerts/{concert['uid']}',
        headers=auth_headers,
        json=concert_update
    )

    assert update_response.status_code == 200
    update_response = update_response.json()
    assert concert_update['artist'] == update_response['artist']
    assert concert_update['tour_name'] == update_response['tour_name']
    assert concert_update['venue'] == update_response['venue']
    assert concert_update['location'] == update_response['location']
    assert concert_update['status'] == update_response['status']

def test_delete(client: TestClient, auth_headers):
    # create concert
    create_reponse = client.post(
        '/concerts/',
        headers=auth_headers,
        json=concert
    )

    # cancel concert
    update_response = client.patch(
        f'/concerts/cancel/{concert['uid']}',
        headers=auth_headers
    )
    assert update_response.status_code == 202

def test_concert_authorization(client: TestClient, auth_headers):
    # create concert
    create_response = client.post(
        '/concerts/',
        headers=auth_headers,
        json=concert
    )

    # try accessing without auth
    endpoints = [
        ('POST', f'/concerts/'),
        ('PATCH', f'/concerts/{concert['uid']}'),
        ('PATCH', f'/concerts/cancel/{concert['uid']}'),
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401

def test_concert_not_found(client: TestClient, auth_headers):
    non_existent_id = ' '

    response = client.get(f'/concerts/id/{non_existent_id}')
    assert response.status_code == 404

    response = client.get(
        f'/concerts/search', 
        params={'concert_id': non_existent_id}
    )
    assert response.status_code == 404

    # response = client.patch(
    #     f'/concerts/{non_existent_id}',
    #     headers=auth_headers,
    #     json=concert_update
    # )
    # assert response.status_code == 404
