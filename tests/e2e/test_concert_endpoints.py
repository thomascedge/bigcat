import json
from fastapi.testclient import TestClient
from src.concerts.model import Concert, ConcertStatus, ConcertResponse
from datetime import datetime
from src.logging import logger

def test_concert_crud_operations(client: TestClient, auth_headers):
    concert = Concert(
        concert_id='TESTCONCERT',
        artist='TESTARTIST',
        tour_name='TESTTOUR',
        venue='TESTVENUE',
        location='TESTLOCATION',
        datetime=datetime(2025, 1, 1),
        status=ConcertStatus.ON_SALE.value
    )

    # create concert
    create_response = client.post(
        '/concerts/',
        headers=auth_headers,
        json=json.dumps(concert.model_dump(), indent=4, sort_keys=True, default=str)
    )
    logger.debug(f'Create response: {create_response}')
    assert create_response.status_code == 201
    create_response = create_response.json()
    assert concert.concert_id == create_response['concert_id']
    assert concert.artist == create_response['artist']
    assert concert.tour_name == create_response['tour_name']
    assert concert.venue == create_response['venue']
    assert concert.location == create_response['location']
    assert concert.datetime == create_response['datetime']
    assert concert.status == create_response['status']

    # get concert
    get_response = client.get(f'/concerts/{concert.concert_id}')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert concert.concert_id == get_response['concert_id']

    # get all concerts
    get_response = client.get(f'/concerts/')
    assert get_response.status_code == 200
    get_response = get_response.json()
    assert len(get_response) > 0
    assert any(concert.concert_id == returned_concert['concert_id'] for returned_concert in get_response)

    # search concert
    params = { 
            'artist': 'TESTARTIST',
            'tour_name': 'TESTTOUR',
            'venue': 'TESTVENUE',
            'location': 'TESTLOCATION',
            'date': datetime(2025, 1, 1)
        }

    search_response = client.get(
        f'/concerts/search',
        params=json.dumps(params, indent=4, sort_keys=True, default=str)
    )
    assert search_response == 200
    search_response = search_response.json()
    assert concert.concert_id == search_response['concert_id']

    # search concert by concert id
    search_response = client.get(
        f'/concerts/search',
        params={ 
            'concert_id': 'TESTCONCERT'
        }
    )
    assert search_response == 200
    search_response = search_response.json()
    assert concert.concert_id == search_response['concert_id']

    # update concert
    concert_update = Concert(
            concert_id='TESTCONCERT',
            artist='TESTARTIST1',
            tour_name='TESTTOUR1',
            venue='TESTVENUE1',
            location='TESTLOCATION1',
            datetime=datetime(2025, 1, 1),
            status=ConcertStatus.COMPLETED.value
        )

    update_response = client.patch(
        f'/concerts/{concert.concert_id}',
        json=json.dumps(concert_update.model_dump(), indent=4, sort_keys=True, default=str)
    )
    assert update_response.status_code == 200
    update_response = update_response.json()
    assert concert_update.artist == update_response['artist']
    assert concert_update.tour_name == update_response['tour_name']
    assert concert_update.venue == update_response['venue']
    assert concert_update.location == update_response['location']
    assert concert_update.status == update_response['status']

    # cancel concert
    cancel_response = client.delete(f'/concert/{concert.concert_id}')
    assert update_response.status_code == 200
    update_response = update_response.json()
    assert update_response['status'] == ConcertStatus.CANCELED.value

def test_concert_authorization(client: TestClient):
    # create concert
    concert = Concert(
        concert_id='TESTCONCERT',
        artist='TESTARTIST',
        tour_name='TESTTOUR',
        venue='TESTVENUE',
        location='TESTLOCATION',
        datetime=datetime(2025, 1, 1),
        status=ConcertStatus.ON_SALE.value
    )

    create_response = client.post(
        '/concerts/',
        json=concert.model_dump()
    )
    concert_id = create_response.concert_id

    # try accessing without auth
    endpoints = [
        ('POST', f'/concerts/'),
        ('PATCH', f'/concerts/{concert_id}'),
        ('DELETE', f'/concerts/{concert_id}'),
    ]

    for method, endpoint in endpoints:
        response = client.request(method, endpoint)
        assert response.status_code == 401


def test_concert_not_found(client: TestClient):
    non_existent_id = ' '

    response = client.get(f'/concerts/{non_existent_id}')
    assert response.status_code == 404

    concert_update = Concert(
            concert_id='TESTCONCERT1',
            artist='TESTARTIST1',
            tour_name='TESTTOUR1',
            venue='TESTVENUE1',
            location='TESTLOCATION1',
            datetime=datetime(2025, 1, 1),
            status=ConcertStatus.COMPLETED.value
        )

    response = client.put(f'/concerts/{non_existent_id}', json=concert_update.model_dump())
    assert response.status_code == 404

    response = client.delete(f'/concerts/{non_existent_id}')
    assert response.status_code == 404
