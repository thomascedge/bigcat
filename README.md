# 🐈‍⬛ bigcat

bigcat is a concert ticketing system similar to Ticketmaster or Eventbrite. The purpose of this project is to display and expand my API buidling and systems architecture skills. Born from the [booking system outline](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/concert-ticket-booking-system.md) low-level design challenge, this code uses it as a schema for building out a robust API.

## Play with bigcat

To run, use this following command. Please send me a message hello@thomascedge.com for an account login and the url. Otherwise feel free to run the Dockerfile on your machine and use any of the requests that do not require authorization.

```python

import requests

payload = {
	'email': '<YOUR_EMAIL>',
	'password': '<YOUR_PASSWORD>',
	'grant_type: 'password'
}

response = requests.post(f'{base_url}/auth/token', data=payload)

if response.status_code == 200:
    data = response.json()
    token = data['access_token']
    print('Successfully signed in.')

    headers = {"Authorization": f"Bearer {token}"}
else:
    print('Cannot login. Please ensure credentials are correct.')
```

## Endpoints
Below is a list of example endpoints. All GET endpoints are listed.
| Method | Endpoint                  | Description                                                                                                | Requires Authorization |
|--------|---------------------------|------------------------------------------------------------------------------------------------------------|------------------------|
| GET    | /bookings                 | Gets all bookings from database.                                                                           | ✅                     |
| GET    | /bookings/{booking_id}    | Searches database for individual concert based on booking_id.                                              | ✅                     |
| GET    | /concerts                 | Gets all concerts from database.                                                                           |                        |
| GET    | /concerts/id/{concert_id} | Searches database for individual concert based on concert_id.                                              |                        |
| GET    | /concerts/search?...      | Searches database for concert based on query params: artist, tour_name, venue, location, concert_datetime. |                        |
| GET    | /seats                    | Gets all seats from database.                                                                              |                        |
| GET    | /seats/id/{seat_id}       | Searches database for individual concert based on booking_id.                                              |                        |
