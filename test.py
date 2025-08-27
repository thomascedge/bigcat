from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

''' --------------  GET -------------- '''

def search_artist():
    response = client.get('/concert?artist=haim')
    assert response.status_code == 200

def search_venue_and_date():
    response = client.get('/concert?venue=Emo&date=10-15-2025')
    assert response.status_code == 200

def search_concert_id():
    response = client.get('/concert?concert_id=HAIMHTX2025')
    assert response.status_code == 404


''' --------------  POST -------------- '''

def successful_booking():
    response = client.post(
        "/booking",
        json={
                "user_id": "68add8527d9506dd5708b065",
                "concert_id": "SMTBATX2025",
                "seats": ["68ae3665743ec4686ef64bc0", "68ae3665743ec4686ef64bc1"]
              },
    )
    assert response.status_code == 200

def booking_wrong_user_id():
    response = client.post(
        "/booking",
        json={
                "user_id": "342dd8287d9506dd5708b064",
                "concert_id": "HAIMATX2025",
                "seats": ["68ae3665743ec4686ef64bc0", "68ae3665743ec4686ef64bc1"]
            },
    )
    assert response.status_code == 404

def booking_wrong_concert_id():
    response = client.post(
        "/booking",
        json={
                "user_id": "68add8287d9506dd5708b064",
                "concert_id": "HAIMATX2023",
                "seats": ["68ae3665743ec4686ef64bc0", "68ae3665743ec4686ef64bc1"]
            },
    )
    assert response.status_code == 404

def booking_wrong_no_more_tickets():
    response = client.post(
        "/booking",
        json={
                "user_id": "68add8287d9506dd5708b064",
                "concert_id": "SMTBATX2025",
                "seats": ["68ae3665743ec4686ef64bc0", "68ae3665743ec4686ef64bc1"]
            },
    )
    assert response.status_code == 400


''' --------------  PATCH -------------- '''

def successful_booking_cancelation():
    response = client.patch("booking/68af004676b3a130b2d44402")
    assert response.status_code == 200

def cancel_wrong_booking_id():
    response = client.patch("booking/1011111332d0905d23c53502")
    assert response.status_code == 404

def booking_already_canceled():
    response = client.patch("booking/68af004676b3a130b2d44402")
    assert response.status_code == 200